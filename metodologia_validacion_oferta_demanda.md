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

## Capa salarial

La capa salarial se agrega para estimar el premio economico de cada habilidad/carrera.

Fuentes publicas:

- Nomina Publica General del Estado, MAP / datos.gob.do.
- Escalas salariales institucionales publicadas en portales de transparencia.
- Salario minimo oficial del sector privado no sectorizado y sectores especiales.
- Promedios sectoriales ONE / ENAE.

Fuentes privadas:

- Vacantes con salario explicitamente publicado.
- Bolsas de empleo locales con rangos visibles.
- Encuestas salariales privadas cuando esten disponibles publicamente.
- Computrabajo RD como primera fuente privada operativa, usando vacantes y paginas de categoria que muestran montos mensuales visibles.

Unidad de analisis para sector publico:

- Cargo publico agregado por categoria STEAM.
- Sueldo bruto mensual.
- Conteo de cargos coincidentes.
- Minimo, percentil 25, mediana, promedio, percentil 75 y maximo.

Proteccion metodologica:

- El archivo bruto de nomina no se conserva en el repositorio.
- No se guardan nombres de empleados.
- No se publican registros individuales.
- Solo se guardan agregados por categoria.

Archivos generados:

- `salary_public_sector_latest.json`
- `salary_public_sector_latest.csv`
- `salary_private_jobs_latest.json`
- `salary_private_jobs_latest.csv`
- `salary_private_raw_latest.json`
- `salary_private_raw_latest.csv`
- `salary_reference_baseline.json`

Interpretacion correcta:

> Rangos salariales observados en nomina publica y rangos publicados en vacantes privadas, agregados por categoria STEAM.

No debe presentarse como:

> Salario exacto universal de cada carrera en todo el mercado dominicano.

## Frase recomendada para el informe

> La demanda fue validada mediante una auditoria automatizada de vacantes activas en LinkedIn Jobs RD. La oferta fue validada mediante conteos agregados de LinkedIn People Search filtrados por Republica Dominicana, sin almacenar datos personales. Por tanto, los resultados representan una medicion puntual y reproducible de presencia digital laboral, no un censo nacional exhaustivo.

## Frase recomendada para salarios

> La dimension salarial se calculo mediante agregacion de sueldos brutos mensuales publicados en la Nomina Publica General del Estado y mediante extraccion de rangos explicitamente publicados en vacantes privadas. Los resultados se reportan por categoria STEAM en forma de rangos y medianas, no como remuneraciones individuales ni como censo completo del mercado.
