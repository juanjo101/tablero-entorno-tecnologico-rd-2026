# Metodologia de validacion oferta-demanda STEAM RD

## Objetivo

Validar con evidencia separada la demanda laboral y la oferta de talento para carreras y habilidades STEAM en la Republica Dominicana.

## Demanda

La demanda se mide con vacantes activas capturadas en LinkedIn Jobs para ubicacion Republica Dominicana.

Unidad de analisis:

- Vacante activa.
- Titulo del puesto.
- Empresa.
- Ubicacion/modalidad.
- Categoria STEAM inferida.
- Fecha de captura.

Archivo de evidencia:

- `linkedin_jobs_demand_latest.json`
- `linkedin_jobs_demand_latest.csv`
- Versiones historicas `linkedin_jobs_demand_YYYYMMDD_HHMM.*`

Interpretacion correcta:

> Demanda observada en vacantes activas publicadas en LinkedIn Jobs al momento de la captura.

No debe presentarse como:

> Total absoluto de todos los empleos STEAM existentes en el pais.

## Oferta

La oferta se mide con conteos agregados de LinkedIn People Search por habilidad/carrera, filtrados por Republica Dominicana.

Unidad de analisis:

- Conteo agregado de resultados por busqueda.
- Habilidad/carrera consultada.
- URL parametrizada de busqueda.
- Fecha de captura.
- Indice de oferta normalizado contra el mayor conteo de la muestra.

Archivo de evidencia:

- `linkedin_profile_supply_latest.json`
- Versiones historicas `linkedin_profile_supply_YYYYMMDD_HHMM.*`

Proteccion metodologica:

- No se guardan nombres.
- No se guardan URLs de perfiles.
- No se guardan cargos individuales.
- Solo se guardan conteos agregados por habilidad.

Interpretacion correcta:

> Presencia relativa de perfiles LinkedIn ubicados en Republica Dominicana que declaran o coinciden con una habilidad/carrera.

No debe presentarse como:

> Censo exacto nacional de profesionales.

## Cruce oferta-demanda

El mapa de brechas compara:

- Demanda: intensidad de vacantes y tendencias de mercado.
- Oferta: presencia relativa de perfiles por habilidad/carrera.

La brecha se interpreta como:

> Riesgo de insuficiencia relativa de talento disponible frente a la demanda observada.

## Frase recomendada para el informe

> La demanda fue validada mediante una auditoria automatizada de vacantes activas en LinkedIn Jobs RD. La oferta fue validada mediante conteos agregados de LinkedIn People Search filtrados por Republica Dominicana, sin almacenar datos personales. Por tanto, los resultados representan una medicion puntual y reproducible de presencia digital laboral, no un censo nacional exhaustivo.

