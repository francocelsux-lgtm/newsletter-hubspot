# Análisis de campaña: Newsletter Celsux 105

**Fecha de envío:** 17/7/2026

**Fuente de datos:** CSV histórico entregado por Franco ("Métricas Newsletter"), fila del newsletter 105. Mismas limitaciones que el resto de la serie.

## Números crudos

| Métrica | Valor |
|---|---|
| Entregados | 744 de 744 enviados |
| Abiertos | 20,70% (154 únicos) |
| Clics | 0,27% (2 únicos) |
| Click-to-open | 1,30% |
| Rebotes | 0,00% (0 de 744) |
| Bajas | 1,21% (9 de 744) |

## Comparación contra la campaña anterior

Respecto al 104: el open rate baja de nuevo (24,16% → 20,70%, el más bajo de toda la serie hasta acá), pero el click-to-open mejora (0,56% → 1,30%). El rebote vuelve a 0% y las bajas suben un poco (0,13% → 1,21%).

## Hallazgos [con nivel de confianza en cada uno]

- [SEGURO] Open rate de 20,70% es el más bajo registrado en la serie 101-105 — vale la pena revisar si hubo un cambio de asunto o de horario de envío en este newsletter puntual.
- [SEGURO] A pesar del open rate más bajo, el click-to-open mejora respecto a 104 (0,56% → 1,30%) — de las pocas personas que abrieron, proporcionalmente más clickearon. Sigue lejos del benchmark de 10-20%.
- [PROBABLE] El aumento de bajas (1,21% contra 0,13% del envío anterior) podría estar relacionado con el open rate más bajo, pero no hay dato suficiente para asegurar causalidad.

## Contradice o confirma algún aprendizaje anterior

- **Confirma entrada 1** ([SEGURO]): click-to-open otra vez muy por debajo del benchmark sano.
- **Confirma entrada 5** ([SEGURO]): rebote en 0%, sin problema de entrega.

## Qué probar en la próxima campaña

1. Revisar el asunto y horario de envío de este newsletter puntual contra los anteriores, dado que tuvo el open rate más bajo de la serie — para descartar que haya sido un problema de asunto antes de seguir iterando el CTA.

## Propuesta de actualización a ACUMULADO.md

No propongo entrada nueva — confirma lo ya anotado.

---

**Nota aparte:** el siguiente análisis cronológico ya cargado en `analisis/` es el del newsletter 106 (`semanal-2026-07-31.md`), generado por la primera corrida del chequeo semanal automático, antes de que este historial 101-105 se cargara. Por eso ese análisis dice "no hay análisis previo", lo cual ya no es exacto en retrospectiva — no lo modifiqué para no tocar un archivo ya commiteado sin que se pida explícitamente.
