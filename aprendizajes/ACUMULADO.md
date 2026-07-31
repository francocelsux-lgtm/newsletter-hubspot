# Aprendizajes acumulados — Marketing Celsux

Lista viva. Cada entrada indica de qué campaña salió y con qué nivel de confianza se sostiene. Cuando una campaña nueva confirma un aprendizaje, se anota la fecha al lado. Cuando lo contradice, se marca la contradicción en vez de borrar el aprendizaje anterior.

---

### 1. El click-to-open es la métrica que más duele, no el open rate
**Origen:** análisis agregado de base histórica (jul 2026)
**Confianza:** [SEGURO]
Open rate 24,9% (aceptable), pero click-to-open de apenas 2,2% contra un benchmark sano de 10-20%. El problema no está en el asunto, está en el cuerpo del mail y el CTA.

### 2. Segmentar por etapa del contacto cambia el resultado a la mitad
**Origen:** análisis agregado de base histórica (jul 2026)
**Confianza:** [SEGURO]
Contactos en etapa "Opportunity" abren casi el doble (45,5%) y clickean el triple (1,36%) que los "Lead" fríos (23,8% / 0,44%). Mandar el mismo mail a toda la base diluye el promedio real.

### 3. La bandeja genérica (info@/hola@/contacto@) no es una señal de interés
**Origen:** caso El Brocal de San Pedro (jul 2026)
**Confianza:** [SEGURO]
Un click desde una casilla genérica, sin nombre ni historial previo, y con apertura+clic separados por segundos, es ruido de bandeja compartida. No activar research completo ni propuesta de alto ticket solo por esta señal.

### 4. 3,7% de opt-out acumulado es alto para el tamaño de la base
**Origen:** análisis agregado de base histórica (jul 2026)
**Confianza:** [SEGURO]
29 de 784 contactos se dieron de baja de todo. Revisar si se está mezclando newsletter + cold email sobre las mismas personas sin coordinar frecuencia.

### 5. El deliverability no es el problema hoy
**Origen:** análisis agregado de base histórica (jul 2026)
**Confianza:** [SEGURO]
Bounce de 0,1% (4 de 3.938). Cualquier problema de performance en los mails es de contenido/segmentación, no de infraestructura de envío, al menos por ahora.

### 6. Falta cargar `celsux_tipo_mail` en la base
**Origen:** análisis agregado de base histórica (jul 2026)
**Confianza:** [PROBABLE]
Solo 2 de 784 contactos tienen esa etiqueta cargada. Sin eso no se puede medir qué etapa de la secuencia de cold email convierte mejor. Es un problema operativo, no de las campañas en sí.

---

## Limitaciones conocidas de esta fuente de datos

- El CRM conectado no tiene permisos para leer `CAMPAIGN` ni `MARKETING_EMAIL` (piden reautorización / upgrade de cuenta). El análisis agregado usa propiedades a nivel contacto, no el desglose por campaña individual desde HubSpot. Si se sube un export manual de la campaña (CSV/captura), ese sí permite análisis específico de esa campaña puntual.
