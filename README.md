# Repo de Análisis de Campañas de Marketing — Celsux

Este repo guarda cada campaña de marketing que sale de Celsux y el análisis de datos correspondiente, para que los aprendizajes queden acumulados en un solo lugar y se puedan reusar al armar la próxima campaña.

## Estructura

```
campanas/       -> lo que se subió de cada campaña (export de HubSpot, capturas, notas, briefs)
analisis/       -> un archivo markdown por campaña, con el análisis de datos completo
aprendizajes/   -> ACUMULADO.md, la lista viva de claves que se van sumando campaña a campaña
plantilla-analisis.md -> estructura que sigue cada análisis nuevo
.github/workflows/analizar-campana.yml -> el workflow que dispara el análisis automático
scripts/analizar_campana.py -> arma el prompt, llama a Claude y escribe el análisis
```

## Cómo se dispara el flujo (automático)

1. Fran sube la campaña nueva a `campanas/AAAA-MM-nombre-campana/` (export CSV de HubSpot, capturas, notas o brief) y hace push.
2. Eso dispara el GitHub Action `analizar-campana.yml` (corre en cualquier rama por default; se puede restringir a la rama principal editando el `branches:` comentado en el workflow), que:
   - Detecta qué subcarpeta(s) de `campanas/` cambiaron en el push.
   - Para cada una, corre `scripts/analizar_campana.py`, que lee todos los archivos de esa campaña, `plantilla-analisis.md`, `aprendizajes/ACUMULADO.md` y el análisis más reciente que ya exista en `analisis/`.
   - Llama a la API de Anthropic (modelo configurado en el workflow) para generar el análisis siguiendo exactamente la plantilla.
   - Escribe `analisis/<nombre-campaña>.md` con ese contenido, incluyendo al final una sección **"Propuesta de actualización a ACUMULADO.md"** con los cambios sugeridos a los aprendizajes (propuestos, no aplicados).
   - Abre un Pull Request con el/los archivo(s) de análisis nuevos.
3. Fran revisa el PR: chequea que las métricas coincidan con el archivo fuente y decide si acepta la propuesta de actualización a `ACUMULADO.md` (si la acepta, copia esas entradas a mano dentro de `aprendizajes/ACUMULADO.md`, en el mismo PR o en un commit aparte).
4. Al mergear el PR queda el análisis (y, si corresponde, el `ACUMULADO.md` actualizado) en `main`.

También se puede disparar a mano desde la pestaña **Actions → Analizar campaña de marketing → Run workflow**, indicando el nombre exacto de la subcarpeta en `campanas/` a re-analizar.

### Secret que hay que configurar

El workflow necesita una API key de Anthropic para poder llamar al modelo:

1. Ir a **Settings → Secrets and variables → Actions** en este repo.
2. Crear un secret nuevo llamado `ANTHROPIC_API_KEY` con el valor de la API key.

Sin ese secret, el paso de análisis falla explícitamente (no se genera un análisis a medias).

Si tu organización no permite que las Actions abran Pull Requests por default, hay que habilitarlo en **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**.

El modelo usado (`claude-sonnet-5` por default) se configura en la variable `ANTHROPIC_MODEL` dentro de `.github/workflows/analizar-campana.yml`, por si hay que cambiarlo más adelante.

## Reglas del análisis

- Cada afirmación va etiquetada [SEGURO], [PROBABLE] o [SUPOSICIÓN], según qué tan sólida es la evidencia. Nunca se marca como [SEGURO] algo que en realidad es una inferencia.
- El hallazgo más incómodo o más crítico va primero en el análisis, no al final.
- Si falta un dato para calcular una métrica de la plantilla (por ejemplo, una columna que HubSpot no exportó), el análisis lo dice explícitamente en vez de estimarlo.
- Si un dato de una campaña nueva contradice un aprendizaje ya anotado en `ACUMULADO.md`, se marca la contradicción explícitamente en vez de promediar o ignorarla.
- Las adiciones a `ACUMULADO.md` nunca se aplican solas: quedan propuestas al final del análisis para que alguien las revise y las copie a mano.
- Los aprendizajes de `ACUMULADO.md` están para consultarse antes de escribir el copy de una campaña nueva, no solo para archivarse.

## Chequeo semanal automático (Routine, vía conector de HubSpot)

Además del flujo disparado por push, hay una **Routine de Claude Code** (no vive como código en este repo, se administra desde la plataforma) que corre todos los lunes 9:00 (hora Argentina):

1. Arranca una sesión nueva de Claude con acceso al repo y al conector de HubSpot.
2. Lee `plantilla-analisis.md`, `aprendizajes/ACUMULADO.md` y el análisis más reciente en `analisis/`.
3. Intenta traer datos de campañas individuales desde HubSpot. Si la cuenta no tiene permiso para leer `CAMPAIGN`/`MARKETING_EMAIL` (la limitación ya documentada en `ACUMULADO.md`), cae automáticamente a los datos agregados a nivel contacto y lo dice explícitamente en el análisis — nunca inventa el desglose por campaña.
4. Escribe `analisis/semanal-AAAA-MM-DD.md` con las mismas reglas de siempre (etiquetas de confianza, hallazgo más crítico primero, sin inventar columnas) y agrega al final la sección "Propuesta de actualización a ACUMULADO.md".
5. Abre un Pull Request — **nunca mergea sola**. Esa es la instancia de revisión manual que se mantiene a propósito.
6. Cuando termina, llega un mail de resumen a `franco@celsux.com.ar` avisando que hay algo para revisar.

**Limitación activa:** al crearla, la plataforma no permitió adjuntarle el conector de HubSpot a esta Routine ("connectors parameter is not available for this organization"), así que por ahora las corridas semanales van a correr sin acceso real a HubSpot y lo van a reportar explícitamente en vez de simular datos. Para habilitarlo, hay que crear o editar esta Routine desde la propia UI de Routines en claude.ai (ahí sí se puede asociar el conector de HubSpot a mano) o resolverlo con un admin de la organización.

## Flujo manual (alternativa)

Si preferís pedir el análisis a mano en vez de esperar al push:

1. Subí la campaña a `campanas/AAAA-MM-nombre-campana/`.
2. En el chat con Claude, pedí el análisis de esa campaña puntual.
3. Claude arma el archivo en `analisis/` siguiendo `plantilla-analisis.md`, y revisa si algo confirma o contradice `aprendizajes/ACUMULADO.md`.
4. Hacé commit y push de los archivos nuevos.
