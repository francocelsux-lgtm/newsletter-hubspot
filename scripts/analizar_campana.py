#!/usr/bin/env python3
"""
Arma el prompt de análisis de una campaña, llama a la API de Anthropic
y escribe el resultado en analisis/<campaña>.md.

Se ejecuta desde el workflow .github/workflows/analizar-campana.yml, uno
por cada carpeta de campaña que haya cambiado en el push. Toda la lógica
de qué se le pide al modelo vive acá, no en el YAML.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MAX_TOKENS = 8192

# Límite de caracteres por archivo y por campaña para no pasarnos de contexto.
# Si un CSV lo supera, se trunca y se avisa explícitamente en el prompt
# (nunca se manda un archivo "resumido" en silencio).
MAX_CHARS_PER_FILE = 150_000
MAX_CHARS_TOTAL = 300_000

SYSTEM_PROMPT = """\
Sos el analista de marketing que audita las campañas de email de Celsux.
Tu trabajo es leer los datos crudos de una campaña nueva y escribir el
archivo de análisis correspondiente. Reglas que no podés romper:

1. Estructura: seguí EXACTAMENTE los encabezados y el orden de la plantilla
   que te paso más abajo. No agregues secciones nuevas dentro del cuerpo
   principal (la única sección extra permitida es la de propuesta de
   actualización a ACUMULADO.md, al final, como se indica más abajo).

2. No inventes columnas ni datos de HubSpot. Si para calcular una métrica
   de la plantilla falta la columna o el dato correspondiente en los
   archivos de la campaña que te paso, escribilo explícitamente como
   "No disponible: falta [dato] en el archivo entregado" en vez de
   estimarlo, inferirlo o completarlo con un valor típico.

3. Etiquetá CADA afirmación con [SEGURO], [PROBABLE] o [SUPOSICIÓN]:
   - [SEGURO]: sale directo de un número presente en los archivos, sin
     ambigüedad ni interpretación de por medio.
   - [PROBABLE]: es una lectura razonable de los datos pero implica
     interpretación, comparación indirecta o un supuesto menor.
   - [SUPOSICIÓN]: es una hipótesis con evidencia débil o indirecta.
   Nunca marques como [SEGURO] algo que en realidad es una inferencia tuya.

4. Tono directo: en la sección de Hallazgos, el hallazgo más incómodo o
   más crítico va PRIMERO, no al final. No suavices ni escondas un
   resultado malo en el medio del texto.

5. Comparación contra la campaña anterior: si te paso el análisis anterior
   más reciente, comparalo métrica por métrica y decí si sube, baja o se
   mantiene. Si no te paso ningún análisis anterior, decilo explícitamente
   ("Es la primera campaña analizada, no hay base de comparación") y no
   inventes una comparación.

6. Aprendizajes acumulados: te paso el contenido completo de
   aprendizajes/ACUMULADO.md. En la sección "Contradice o confirma algún
   aprendizaje anterior" de la plantilla, revisá cada entrada relevante y
   decí explícitamente si esta campaña la confirma, la contradice, o no
   aporta evidencia sobre ella. Citá el número de entrada de ACUMULADO.md.

7. Al final del archivo, después de haber completado toda la plantilla,
   agregá una sección nueva con exactamente este título:

   ## Propuesta de actualización a ACUMULADO.md

   Ahí proponé (sin darlas por aplicadas) las adiciones, ediciones o
   contradicciones a marcar en ACUMULADO.md a partir de esta campaña, con
   el mismo formato de entrada que ya usa ese archivo (origen, nivel de
   confianza, texto). Si esta campaña no aporta nada nuevo para
   ACUMULADO.md, decilo explícitamente en esa sección en vez de omitirla.

Devolvé ÚNICAMENTE el contenido del archivo markdown final, arrancando
directo con el encabezado "# Análisis de campaña: ...". Sin comentarios
antes o después, sin envolver todo en un bloque de código.
"""


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def collect_campaign_files(campaign_dir: Path) -> list[tuple[str, str]]:
    files = []
    for path in sorted(campaign_dir.rglob("*")):
        if path.is_dir() or path.name == ".gitkeep":
            continue
        rel = path.relative_to(campaign_dir).as_posix()
        content = read_text_file(path)
        if len(content) > MAX_CHARS_PER_FILE:
            content = (
                content[:MAX_CHARS_PER_FILE]
                + f"\n\n[ARCHIVO TRUNCADO: se muestran los primeros "
                f"{MAX_CHARS_PER_FILE} caracteres de {len(content)} totales. "
                f"No asumas datos de la parte no incluida.]"
            )
        files.append((rel, content))
    return files


def enforce_total_budget(files: list[tuple[str, str]]) -> list[tuple[str, str]]:
    total = 0
    result = []
    for rel, content in files:
        if total >= MAX_CHARS_TOTAL:
            result.append(
                (rel, "[ARCHIVO OMITIDO: se alcanzó el límite total de "
                      "caracteres de la campaña. No asumas datos de este archivo.]")
            )
            continue
        remaining = MAX_CHARS_TOTAL - total
        if len(content) > remaining:
            content = content[:remaining] + "\n\n[ARCHIVO TRUNCADO por límite total de la campaña.]"
        total += len(content)
        result.append((rel, content))
    return result


def find_previous_analysis(previous_list_path: Path | None, analisis_dir: Path, exclude_filename: str) -> tuple[str, str] | None:
    if previous_list_path and previous_list_path.exists():
        names = [
            Path(line.strip()).name
            for line in previous_list_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        names = [p.name for p in analisis_dir.glob("*.md")]

    candidates = sorted(
        n for n in set(names) if n != exclude_filename and n != "plantilla-analisis.md"
    )
    if not candidates:
        return None

    latest_name = candidates[-1]
    latest_path = analisis_dir / latest_name
    if not latest_path.exists():
        return None
    return latest_name, read_text_file(latest_path)


def build_user_message(
    campaign_name: str,
    template: str,
    acumulado: str,
    previous: tuple[str, str] | None,
    campaign_files: list[tuple[str, str]],
) -> str:
    parts = []

    parts.append(
        "PLANTILLA A SEGUIR (usá esta estructura exacta, mismos encabezados y orden):\n"
        f"{template}"
    )

    parts.append(
        "APRENDIZAJES ACUMULADOS HASTA AHORA (aprendizajes/ACUMULADO.md):\n"
        f"{acumulado}"
    )

    if previous:
        prev_name, prev_content = previous
        parts.append(
            f"ANÁLISIS ANTERIOR MÁS RECIENTE EN analisis/ (archivo: {prev_name}), "
            f"usalo para la sección de comparación:\n{prev_content}"
        )
    else:
        parts.append(
            "No hay ningún análisis previo en analisis/. Es la primera campaña "
            "analizada: decilo explícitamente en la sección de comparación y no "
            "inventes una base de comparación."
        )

    files_block = "\n\n".join(
        f"--- archivo: {rel} ---\n{content}" for rel, content in campaign_files
    )
    if not files_block:
        files_block = "(la carpeta de la campaña no tiene archivos legibles)"
    parts.append(
        f"ARCHIVOS DE LA CAMPAÑA NUEVA A ANALIZAR ('{campaign_name}', "
        f"carpeta campanas/{campaign_name}/):\n{files_block}"
    )

    parts.append(
        f'Nombre de la campaña a usar en el título del análisis: "{campaign_name}".'
    )

    return "\n\n".join(parts)


def call_anthropic(api_key: str, model: str, system_prompt: str, user_message: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "max_tokens": MAX_TOKENS,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=body,
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"Error llamando a la API de Anthropic ({e.code}): {detail}"
        )

    content_blocks = payload.get("content", [])
    text_parts = [b["text"] for b in content_blocks if b.get("type") == "text"]
    if not text_parts:
        raise SystemExit(f"Respuesta sin contenido de texto: {payload}")
    return "\n".join(text_parts).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign-name", required=True, help="Nombre de la carpeta en campanas/")
    parser.add_argument("--campaign-dir", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--acumulado", required=True, type=Path)
    parser.add_argument("--analisis-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--previous-list",
        type=Path,
        default=None,
        help="Archivo con la lista de analisis/*.md existentes ANTES de esta corrida "
        "(evita que una campaña generada en el mismo run se cuente como 'anterior' de otra).",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Falta la variable de entorno ANTHROPIC_API_KEY.")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    if not args.campaign_dir.is_dir():
        raise SystemExit(f"No existe la carpeta de campaña: {args.campaign_dir}")

    template = read_text_file(args.template)
    acumulado = read_text_file(args.acumulado)

    campaign_files = collect_campaign_files(args.campaign_dir)
    campaign_files = enforce_total_budget(campaign_files)
    if not campaign_files:
        raise SystemExit(
            f"La carpeta {args.campaign_dir} no tiene archivos legibles para analizar."
        )

    output_filename = args.output.name
    previous = find_previous_analysis(args.previous_list, args.analisis_dir, output_filename)

    user_message = build_user_message(
        args.campaign_name, template, acumulado, previous, campaign_files
    )

    print(f"Analizando campaña '{args.campaign_name}' con {len(campaign_files)} archivo(s)...")
    if previous:
        print(f"Comparando contra análisis previo: {previous[0]}")
    else:
        print("Sin análisis previo: se marcará como primera campaña.")

    result = call_anthropic(api_key, model, SYSTEM_PROMPT, user_message)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"Análisis escrito en {args.output}")


if __name__ == "__main__":
    main()
