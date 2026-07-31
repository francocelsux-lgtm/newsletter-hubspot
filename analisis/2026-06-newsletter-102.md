# Análisis de campaña: Newsletter Celsux 102

**Fecha de envío:** 24/6/2026

**Fuente de datos:** CSV histórico entregado por Franco ("Métricas Newsletter"), fila del newsletter 102. Mismas limitaciones que el 101 (sin distinción de bots, sin desglose por contacto o link).

## Números crudos

| Métrica | Valor |
|---|---|
| Entregados | 777 de 845 enviados |
| Abiertos | 22,91% (178 únicos) |
| Clics | 0,13% (1 único) |
| Click-to-open | 0,56% |
| Rebotes | 8,05% (68 de 845 enviados) |
| Bajas | 2,83% (22 de 777) |

## Comparación contra la campaña anterior

Respecto al newsletter 101: el rebote sube fuerte (3,24% → 8,05%), el open rate baja (39,11% → 22,91%, aunque puede ser efecto de la base mucho más grande), y el click-to-open se derrumba (8,57% → 0,56%).

## Hallazgos [con nivel de confianza en cada uno]

- [SEGURO] El rebote de este envío (8,05%, 68 de 845) es el más alto de toda la serie 101-106 — muy por encima del resto (que ronda 0-3%). Esto **contradice directamente la entrada 5 de `ACUMULADO.md`** ("el deliverability no es el problema hoy"): al menos en este envío puntual, sí lo fue.
- [SEGURO] El click-to-open de este envío (0,56%) es el peor de toda la serie — de 178 personas que abrieron, solo 1 clickeó.
- [PROBABLE] La combinación de alto rebote + bajísimo click-to-open en el mismo envío sugiere un problema de calidad de lista en esta tanda específica (contactos inválidos o desactualizados), no necesariamente de contenido — pero no hay detalle por contacto para confirmarlo.

## Contradice o confirma algún aprendizaje anterior

- **Contradice la entrada 5** ([SEGURO]): "el deliverability no es el problema hoy" no se sostiene para este envío puntual — 8,05% de rebote es un problema real de entrega, no de contenido/segmentación.
- Sin evidencia sobre el resto de las entradas.

## Qué probar en la próxima campaña

1. Revisar la lista usada en este envío puntual: si el 8,05% de rebote viene concentrado en un segmento importado o no verificado, limpiarlo antes del próximo envío a esa fuente.
2. Si el problema de lista se repite en otros newsletters, considerar una verificación de emails antes de enviar, no solo confiar en el rebote post-envío para detectarlo.

## Propuesta de actualización a ACUMULADO.md

- [PROBABLE] Matizar la entrada 5: el rebote no es sistemáticamente bajo — el newsletter 102 (24/6/2026) tuvo 8,05% de rebote, muy por encima del resto de la serie. Sugiero cambiar la afirmación a "el deliverability no es un problema recurrente hoy" en vez de una afirmación absoluta, ya que hubo al menos una excepción real y medible.
