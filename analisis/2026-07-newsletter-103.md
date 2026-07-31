# Análisis de campaña: Newsletter Celsux 103

**Fecha de envío:** El CSV dice 1/6/2026, pero esa fecha es anterior a la del newsletter 101 (17/6) y 102 (24/6), lo cual no es consistente con la numeración secuencial. Es probable que sea un error de carga y la fecha real sea 1/7/2026, pero no lo doy por hecho — queda marcado como [SUPOSICIÓN] hasta confirmarlo con Franco. El resto de este análisis usa el orden numérico de newsletter (103, entre 102 y 104), no la fecha del CSV.

**Fuente de datos:** CSV histórico entregado por Franco ("Métricas Newsletter"), fila del newsletter 103. Mismas limitaciones que el resto de la serie (sin distinción de bots, sin desglose por contacto o link).

## Números crudos

| Métrica | Valor |
|---|---|
| Entregados | 761 de 761 enviados |
| Abiertos | 29,96% (228 únicos) |
| Clics | 0,66% (5 únicos) |
| Click-to-open | 2,19% |
| Rebotes | 0,00% (0 de 761) |
| Bajas | 1,45% (11 de 761) |

## Comparación contra la campaña anterior

Respecto al newsletter 102 (usando el orden numérico, no el de fecha): el rebote vuelve a 0% (contra el 8,05% de 102), el open rate sube (22,91% → 29,96%) y el click-to-open mejora bastante (0,56% → 2,19%), aunque sigue lejos del benchmark sano de 10-20%.

## Hallazgos [con nivel de confianza en cada uno]

- [SEGURO] Rebote en 0% — el problema de deliverability del newsletter 102 no se repitió acá.
- [SEGURO] Click-to-open de 2,19%, muy por debajo del benchmark de 10-20% de la entrada 1 de `ACUMULADO.md` — sigue siendo el patrón dominante de la serie.
- [SUPOSICIÓN] La fecha de envío registrada en el CSV (1/6/2026) es probablemente un error de tipeo — ver nota arriba.

## Contradice o confirma algún aprendizaje anterior

- **Confirma entrada 1** ([SEGURO]): click-to-open muy por debajo del benchmark, otra vez.
- **Confirma entrada 5** para este envío puntual ([SEGURO]): rebote 0%, sin problema de entrega — a diferencia del 102 inmediato anterior.

## Qué probar en la próxima campaña

1. Confirmar con Franco la fecha real de este envío para no arrastrar el error en futuras comparaciones cronológicas.

## Propuesta de actualización a ACUMULADO.md

No propongo entrada nueva — confirma lo ya anotado en las entradas 1 y 5 sin agregar información cualitativa nueva.
