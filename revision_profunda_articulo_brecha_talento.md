<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Revisión por Pares Profunda - Brecha Sociotécnica</title>
<style>
:root{
  --azul:#1d4fa6;
  --azul-claro:#eaf2ff;
  --rojo:#a12323;
  --amarillo:#a96500;
  --verde:#1b6b45;
  --gris:#dbe3ef;
  --texto:#243044;
}
body{
  margin:0;
  font-family:Arial, Helvetica, sans-serif;
  background:linear-gradient(135deg,#edf4ff,#f6f8fb);
  color:var(--texto);
  line-height:1.65;
}
.wrapper{
  display:flex;
  max-width:1500px;
  margin:0 auto;
}
aside{
  width:270px;
  background:#ffffff;
  border-right:1px solid var(--gris);
  padding:24px;
  position:sticky;
  top:0;
  height:100vh;
  overflow:auto;
}
aside h2{
  color:var(--azul);
  font-size:18px;
}
aside a{
  display:block;
  color:#243044;
  text-decoration:none;
  padding:7px 0;
  border-bottom:1px solid #eef2f7;
}
main{
  flex:1;
  padding:30px;
}
.hero{
  background:linear-gradient(135deg,#1d4fa6,#4c7ed8);
  color:#fff;
  border-radius:18px;
  padding:34px;
  box-shadow:0 14px 35px rgba(29,79,166,.25);
}
.hero h1{
  margin:0;
  color:#fff;
  font-size:32px;
}
.hero p{
  margin:10px 0 0;
  font-size:16px;
}
button{
  background:#fff;
  color:var(--azul);
  padding:12px 18px;
  border:0;
  border-radius:8px;
  font-weight:bold;
  margin-top:18px;
  cursor:pointer;
}
.card{
  background:#fff;
  border:1px solid var(--gris);
  border-radius:16px;
  margin:22px 0;
  padding:24px;
  box-shadow:0 8px 20px rgba(0,0,0,.05);
}
h1,h2,h3{
  color:var(--azul);
}
.callout{
  padding:16px;
  margin:14px 0;
  border-radius:10px;
}
.red{background:#fdeaea;border-left:7px solid var(--rojo);}
.yellow{background:#fff5df;border-left:7px solid var(--amarillo);}
.green{background:#eaf8ef;border-left:7px solid var(--verde);}
.blue{background:var(--azul-claro);border-left:7px solid var(--azul);}
.rewrite{
  background:#f8fafc;
  border:1px dashed #9aa8bd;
  padding:16px;
  border-radius:10px;
  margin-top:12px;
}
.original{color:var(--rojo);font-weight:bold;}
.problem{color:var(--amarillo);font-weight:bold;}
.fixed{color:var(--verde);font-weight:bold;}
.just{color:var(--azul);font-weight:bold;}
table{
  width:100%;
  border-collapse:collapse;
  margin:18px 0;
  font-size:14px;
}
th,td{
  border:1px solid var(--gris);
  padding:10px;
  vertical-align:top;
}
th{
  background:var(--azul-claro);
  color:var(--azul);
}
.score{
  margin:14px 0;
}
.bar{
  background:#dbe3ef;
  border-radius:999px;
  overflow:hidden;
  height:22px;
}
.fill{
  height:22px;
  background:linear-gradient(90deg,#1d4fa6,#6e9bf0);
}
.badge{
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  font-size:12px;
  font-weight:bold;
}
.badge-red{background:#fdeaea;color:var(--rojo);}
.badge-yellow{background:#fff5df;color:var(--amarillo);}
.badge-green{background:#eaf8ef;color:var(--verde);}
pre{
  white-space:pre-wrap;
  background:#f8fafc;
  border:1px solid var(--gris);
  padding:16px;
  border-radius:10px;
}
@media print{
  aside{display:none}
  main{padding:0}
  body{background:#fff}
  .card,.hero{box-shadow:none}
}
</style>
</head>
<body>
<div class="wrapper">
<aside>
<h2>Índice</h2>
<a href="#resumen">1. Resumen ejecutivo</a>
<a href="#valoracion">2. Valoración editorial</a>
<a href="#fortalezas">3. Fortalezas</a>
<a href="#debilidades">4. Debilidades críticas</a>
<a href="#metodologicos">5. Errores metodológicos críticos</a>
<a href="#secciones">6. Revisión sección por sección</a>
<a href="#reescritura">7. Reescritura directa</a>
<a href="#matriz">8. Matriz correctiva</a>
<a href="#rubrica">9. Rúbrica</a>
<a href="#plan">10. Plan de mejora</a>
<a href="#veredicto">11. Veredicto final</a>
</aside>

<main>
<section class="hero">
<h1>Informe de Revisión por Pares Profunda</h1>
<p><strong>Artículo evaluado:</strong> Brecha sociotécnica entre demanda laboral emergente y oferta académica: un análisis descriptivo-causal en la República Dominicana (2025–2026)</p>
<p><strong>Tipo de dictamen:</strong> Revisión académica senior con enfoque editorial, metodológico, estadístico y APA 7.</p>
<button onclick="window.print()">Imprimir / Guardar PDF</button>
</section>

<section id="resumen" class="card">
<h2>1. Resumen ejecutivo</h2>
<p><strong>Tipo real del artículo:</strong> estudio descriptivo, transversal, comparativo y exploratorio con apoyo documental y análisis de plataformas digitales de empleo. Aunque el texto usa la expresión “descriptivo-causal”, el diseño presentado no permite demostrar relaciones causales en sentido estadístico o inferencial.</p>
<p><strong>Fortaleza principal:</strong> el artículo aborda un problema de alta relevancia nacional: la desalineación entre la demanda tecnológica emergente del mercado dominicano y la oferta académica de educación superior.</p>
<p><strong>Problema principal:</strong> la contribución empírica depende de datos de vacantes, porcentajes de demanda y clasificaciones curriculares que no están suficientemente documentados, reproducidos ni validados.</p>
<p><strong>Dictamen editorial:</strong> <span class="badge badge-red">Revisión mayor</span>. El artículo tiene potencial, pero requiere correcciones sustanciales antes de ser sometido a una revista científica indexada.</p>
</section>

<section id="valoracion" class="card">
<h2>2. Valoración global tipo editor</h2>
<div class="callout blue">
El manuscrito posee una idea valiosa, una narrativa académica sólida y una problemática pertinente. Sin embargo, la estructura metodológica actual no sostiene plenamente la fuerza de las conclusiones. El trabajo debe pasar de una argumentación convincente a una demostración científicamente trazable.
</div>
<table>
<tr><th>Criterio editorial</th><th>Valoración</th><th>Comentario</th></tr>
<tr><td>Originalidad</td><td>Alta</td><td>La relación entre vacantes tecnológicas, currículo universitario y brecha STEAM en RD es pertinente y poco explorada.</td></tr>
<tr><td>Rigor metodológico</td><td>Medio-bajo</td><td>Faltan muestra, criterios de extracción, base de datos, fórmula de porcentajes y validación.</td></tr>
<tr><td>Coherencia conceptual</td><td>Media</td><td>Se mezclan tendencias globales, evidencias locales y proyecciones sin separar claramente sus niveles de inferencia.</td></tr>
<tr><td>Redacción científica</td><td>Alta</td><td>La escritura es fluida, pero en ocasiones adopta tono normativo o categórico.</td></tr>
<tr><td>Publicabilidad</td><td>Condicionada</td><td>Publicable si se corrige la metodología y se documentan los datos.</td></tr>
</table>
</section>

<section id="fortalezas" class="card">
<h2>3. Fortalezas explicadas</h2>
<div class="callout green">
<strong>1. Relevancia nacional:</strong> El tema conecta educación superior, mercado laboral, transformación digital y competitividad nacional.
</div>
<div class="callout green">
<strong>2. Enfoque aplicado:</strong> El artículo no se limita a diagnosticar; propone programas curriculares concretos.
</div>
<div class="callout green">
<strong>3. Uso de un índice propio:</strong> El Índice de Cobertura Curricular representa una buena base para construir una métrica comparativa.
</div>
<div class="callout green">
<strong>4. Integración PESTEL:</strong> El intento de conectar factores económicos, regulatorios y tecnológicos amplía la interpretación del fenómeno.
</div>
</section>

<section id="debilidades" class="card">
<h2>4. Debilidades críticas</h2>
<table>
<tr><th>Debilidad</th><th>Qué está mal</th><th>Impacto científico</th><th>Gravedad</th></tr>
<tr><td>Causalidad no demostrada</td><td>El artículo afirma relaciones causales sin diseño causal.</td><td>Afecta la validez interna y puede generar rechazo editorial.</td><td><span class="badge badge-red">Alta</span></td></tr>
<tr><td>Porcentajes de demanda sin fórmula</td><td>No se explica cómo se obtienen 98%, 96%, 94%, etc.</td><td>Los resultados parecen estimaciones subjetivas.</td><td><span class="badge badge-red">Alta</span></td></tr>
<tr><td>Muestra no reportada</td><td>No se indica cuántas vacantes fueron analizadas.</td><td>Impide evaluar representatividad y replicabilidad.</td><td><span class="badge badge-red">Alta</span></td></tr>
<tr><td>Fuentes no verificables</td><td>Varias referencias no incluyen URL, DOI o datos de recuperación.</td><td>Compromete la trazabilidad bibliográfica.</td><td><span class="badge badge-red">Alta</span></td></tr>
<tr><td>ICC binario limitado</td><td>Trata una carrera completa y una concentración como equivalentes.</td><td>Reduce precisión de la medición curricular.</td><td><span class="badge badge-yellow">Media-alta</span></td></tr>
<tr><td>Confusión evidencia local/global</td><td>Se usan informes globales para reforzar afirmaciones nacionales.</td><td>Puede producir inferencias desproporcionadas.</td><td><span class="badge badge-yellow">Media</span></td></tr>
</table>
</section>

<section id="metodologicos" class="card">
<h2>5. Errores metodológicos críticos</h2>

<div class="callout red">
<h3>5.1. Confusión entre resultados reales y resultados esperados</h3>
<p><strong>Qué está mal:</strong> La tabla de tendencias presenta “demanda proyectada” como si fuese un resultado empírico cerrado.</p>
<p><strong>Por qué está mal:</strong> Si el dato procede de vacantes observadas, debe llamarse frecuencia observada. Si procede de predicción, debe indicarse el modelo de proyección.</p>
<p><strong>Cómo se corrige:</strong> Reemplazar “demanda proyectada” por “frecuencia relativa observada” o explicar el modelo predictivo.</p>
<div class="rewrite">
<span class="original">🔴 Texto original:</span> Demanda Proyectada (%)<br>
<span class="problem">⚠️ Problema:</span> No se reporta modelo de proyección.<br>
<span class="fixed">✅ Versión corregida:</span> Frecuencia relativa de aparición en vacantes analizadas (%)<br>
<span class="just">📌 Justificación:</span> La expresión corregida se ajusta a un estudio descriptivo transversal.
</div>
</div>

<div class="callout red">
<h3>5.2. Muestra insuficientemente descrita</h3>
<p><strong>Qué está mal:</strong> No se reporta número total de vacantes, número de duplicados eliminados, criterios de inclusión, exclusión ni período exacto de captura.</p>
<p><strong>Impacto:</strong> El lector no puede replicar ni validar el estudio.</p>
<p><strong>Corrección:</strong> Añadir una tabla de muestra y procedimiento.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
Durante el período enero–mayo de 2026 se recopilaron vacantes tecnológicas publicadas en plataformas digitales de empleo. Se eliminaron registros duplicados, ofertas sin ubicación verificable en República Dominicana y publicaciones sin descripción funcional del puesto. La muestra final estuvo compuesta por [N] vacantes únicas, clasificadas en categorías tecnológicas mediante una matriz de codificación previamente definida.
</div>
</div>

<div class="callout red">
<h3>5.3. Variables no operacionalizadas</h3>
<p><strong>Qué está mal:</strong> Conceptos como “IA agéntica”, “hiperautomatización”, “DevOps” y “Cloud-native” no tienen definición operacional verificable.</p>
<p><strong>Impacto:</strong> Dos investigadores podrían clasificar de forma distinta la misma vacante.</p>
<p><strong>Corrección:</strong> Crear un diccionario de codificación.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
Para efectos del estudio, una vacante fue clasificada como relacionada con DevOps cuando incluía al menos dos de los siguientes términos o competencias: CI/CD, Docker, Kubernetes, Terraform, Ansible, observabilidad, automatización de despliegues, infraestructura como código o administración de pipelines.
</div>
</div>

<div class="callout red">
<h3>5.4. Ausencia de confiabilidad interevaluador</h3>
<p><strong>Qué está mal:</strong> No se indica si la clasificación de vacantes y programas fue revisada por más de un evaluador.</p>
<p><strong>Impacto:</strong> La codificación puede depender del juicio individual del autor.</p>
<p><strong>Corrección:</strong> Incluir validación por pares o coeficiente Kappa de Cohen.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
La clasificación inicial fue realizada por el investigador principal y posteriormente revisada por un segundo evaluador con experiencia en tecnología educativa. Las discrepancias fueron resueltas por consenso. Se recomienda reportar el coeficiente Kappa de Cohen para estimar la consistencia interevaluador.
</div>
</div>

<div class="callout yellow">
<h3>5.5. Error estadístico potencial</h3>
<p>No se observa uso incorrecto de Alfa de Cronbach porque el artículo no emplea escalas psicométricas. Sin embargo, sí existe un problema estadístico más relevante: se presentan porcentajes sin denominador ni procedimiento de estimación.</p>
</div>
</section>

<section id="secciones" class="card">
<h2>6. Revisión sección por sección</h2>

<h3>6.1. Título</h3>
<p><strong>Evaluación:</strong> atractivo y pertinente, pero metodológicamente impreciso.</p>
<p><strong>Problema:</strong> “descriptivo-causal” sugiere causalidad.</p>
<p><strong>Impacto:</strong> genera expectativa de técnicas causales inexistentes.</p>
<p><strong>Corrección:</strong> cambiar a descriptivo-comparativo.</p>
<div class="rewrite">
<span class="original">🔴 Texto original:</span> Brecha sociotécnica entre demanda laboral emergente y oferta académica: un análisis descriptivo-causal en la República Dominicana (2025–2026).<br>
<span class="fixed">✅ Versión corregida:</span> Brecha sociotécnica entre demanda laboral emergente y oferta académica: análisis descriptivo-comparativo de plataformas digitales de empleo y currículos universitarios en la República Dominicana (2025–2026).<br>
<span class="just">📌 Justificación:</span> La versión corregida delimita mejor el objeto empírico y evita prometer causalidad.
</div>

<h3>6.2. Resumen</h3>
<p><strong>Evaluación:</strong> claro, pero sobredimensiona hallazgos.</p>
<p><strong>Problema:</strong> menciona tasas de adopción y cobertura sin explicar su cálculo.</p>
<p><strong>Impacto:</strong> debilita la confianza del lector en los resultados.</p>
<div class="rewrite">
<span class="fixed">✅ Versión corregida:</span><br>
Este estudio analiza la correspondencia entre competencias tecnológicas demandadas en vacantes digitales y la oferta curricular de grado de nueve instituciones de educación superior dominicanas durante 2025–2026. Se aplicó un diseño descriptivo transversal, basado en la revisión de vacantes publicadas en plataformas digitales de empleo y en el análisis documental de programas académicos vigentes. Para estimar la cobertura académica se calculó un Índice de Cobertura Curricular, complementado con una matriz de brechas por disciplina. Los resultados sugieren una baja cobertura de áreas como ingeniería de datos, DevOps e infraestructura cloud en comparación con su presencia en las vacantes analizadas. Se concluye que la educación superior dominicana requiere fortalecer sus mecanismos de actualización curricular basados en evidencia laboral verificable.
</div>

<h3>6.3. Introducción</h3>
<p><strong>Evaluación:</strong> bien contextualizada, pero extensa y con acumulación de datos.</p>
<p><strong>Problema:</strong> no formula claramente una pregunta de investigación.</p>
<p><strong>Impacto:</strong> dificulta evaluar si los resultados responden al propósito declarado.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
La pregunta que orienta este estudio es: ¿en qué medida la oferta curricular de grado de las principales instituciones dominicanas de educación superior se corresponde con las competencias tecnológicas emergentes observables en las vacantes digitales del mercado laboral dominicano durante 2025–2026?
</div>

<h3>6.4. Problema y objetivos</h3>
<p><strong>Evaluación:</strong> el problema está implícito, pero no estructurado formalmente.</p>
<p><strong>Corrección:</strong> añadir objetivo general y específicos.</p>
<div class="rewrite">
<span class="fixed">✅ Objetivo general sugerido:</span><br>
Determinar el grado de alineación entre la demanda laboral tecnológica observable en plataformas digitales de empleo y la oferta curricular de grado de nueve instituciones de educación superior en la República Dominicana durante el período 2025–2026.<br><br>
<span class="fixed">✅ Objetivos específicos:</span><br>
1. Identificar las competencias tecnológicas emergentes con mayor presencia en vacantes digitales.<br>
2. Clasificar la oferta académica de grado relacionada con dichas competencias.<br>
3. Calcular el nivel de cobertura curricular por disciplina tecnológica.<br>
4. Proponer áreas prioritarias de actualización curricular basadas en las brechas observadas.
</div>

<h3>6.5. Marco teórico</h3>
<p><strong>Evaluación:</strong> amplio y actualizado, pero mezcla evidencia empírica, interpretación prospectiva y recomendaciones de política.</p>
<p><strong>Corrección:</strong> separar antecedentes, marco conceptual y contexto dominicano.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
El marco teórico se organiza en tres niveles: primero, las transformaciones globales del empleo tecnológico; segundo, la relación entre currículo universitario y empleabilidad en economías emergentes; y tercero, el contexto dominicano de digitalización, regulación TIC y formación STEAM.
</div>

<h3>6.6. Metodología</h3>
<p><strong>Evaluación:</strong> es la sección más débil del artículo.</p>
<p><strong>Problema:</strong> no hay suficiente trazabilidad del proceso de recolección y análisis.</p>
<p><strong>Corrección:</strong> reescribir completamente.</p>
<div class="rewrite">
<span class="fixed">✅ Versión corregida:</span><br>
La investigación adoptó un diseño descriptivo, transversal y comparativo. La unidad de análisis laboral estuvo constituida por vacantes tecnológicas publicadas en plataformas digitales de empleo durante el período enero–mayo de 2026. La unidad de análisis curricular estuvo compuesta por programas de grado ofrecidos por nueve instituciones de educación superior dominicanas seleccionadas por su presencia en áreas tecnológicas. Las vacantes fueron clasificadas mediante una matriz de competencias previamente definida. La oferta académica fue codificada según el nivel de presencia curricular de cada disciplina. Para estimar la cobertura se calculó el Índice de Cobertura Curricular y, de manera complementaria, se propone un índice ponderado que distingue entre asignatura aislada, concentración y carrera completa.
</div>

<h3>6.7. Resultados</h3>
<p><strong>Evaluación:</strong> interesantes, pero necesitan respaldo numérico.</p>
<p><strong>Problema:</strong> porcentajes sin denominador.</p>
<p><strong>Corrección:</strong> incluir frecuencia absoluta y relativa.</p>
<div class="rewrite">
<span class="fixed">✅ Formato sugerido de tabla:</span><br>
Tendencia tecnológica | Número de vacantes asociadas | Total de vacantes analizadas | Frecuencia relativa | Nivel de cobertura curricular | Brecha observada
</div>

<h3>6.8. Discusión</h3>
<p><strong>Evaluación:</strong> sólida narrativamente, pero con sobreinterpretación.</p>
<p><strong>Corrección:</strong> usar lenguaje inferencial moderado.</p>
<div class="rewrite">
<span class="original">🔴 Texto original:</span> La alarmante disparidad pone en peligro la sostenibilidad del crecimiento digital dominicano.<br>
<span class="fixed">✅ Versión corregida:</span> La disparidad observada sugiere un riesgo potencial para la disponibilidad futura de talento especializado requerido por procesos de transformación digital en el país.
</div>

<h3>6.9. Conclusiones</h3>
<p><strong>Evaluación:</strong> pertinentes, pero demasiado categóricas.</p>
<div class="rewrite">
<span class="fixed">✅ Versión corregida:</span><br>
Los resultados sugieren la existencia de brechas relevantes entre determinadas competencias tecnológicas emergentes y la oferta curricular de grado analizada. En particular, las áreas de ingeniería de datos, DevOps e infraestructura cloud presentan baja representación curricular frente a su presencia en vacantes digitales. Estos hallazgos justifican la necesidad de estudios longitudinales, validación con empleadores y revisión curricular basada en evidencia.
</div>

<h3>6.10. Limitaciones</h3>
<p><strong>Evaluación:</strong> adecuadas, pero incompletas.</p>
<p><strong>Corrección:</strong> agregar sesgo algorítmico, sesgo de indexación y limitación por falta de entrevistas a empleadores.</p>
<div class="rewrite">
<span class="fixed">✅ Texto sugerido:</span><br>
Una limitación adicional proviene del sesgo algorítmico de las plataformas de empleo, cuyos mecanismos de indexación, visibilidad y recomendación pueden influir en la disponibilidad de vacantes observadas por el investigador. Asimismo, el estudio no incorpora entrevistas directas con empleadores, por lo que las necesidades de talento se infieren a partir de publicaciones digitales y no de declaraciones organizacionales primarias.
</div>

<h3>6.11. Referencias</h3>
<p><strong>Evaluación:</strong> numerosas, pero requieren auditoría.</p>
<p><strong>Problema:</strong> varias referencias parecen informes internos, consultas web o bases de datos no recuperables.</p>
<div class="rewrite">
<span class="fixed">✅ Corrección sugerida:</span><br>
Toda referencia derivada de plataformas digitales debe incluir URL, fecha de recuperación, criterio de búsqueda y, preferiblemente, un repositorio suplementario con capturas o base anonimizada.
</div>

<h3>6.12. Declaración de IA</h3>
<p><strong>Evaluación:</strong> pertinente, pero debe ser más específica.</p>
<div class="rewrite">
<span class="fixed">✅ Versión corregida:</span><br>
El autor declara que utilizó herramientas de inteligencia artificial generativa como apoyo para tareas de depuración textual, organización preliminar de información y asistencia en la estructuración del manuscrito. Las decisiones metodológicas, la interpretación de resultados, la verificación de fuentes y la responsabilidad final del contenido corresponden exclusivamente al autor humano.
</div>
</section>

<section id="reescritura" class="card">
<h2>7. Reescritura directa</h2>

<h3>7.1. Resumen corregido</h3>
<pre>Este estudio analiza la correspondencia entre la demanda laboral tecnológica observable en plataformas digitales de empleo y la oferta curricular de grado de nueve instituciones de educación superior de la República Dominicana durante el período 2025–2026. Se aplicó un diseño descriptivo, transversal y comparativo, basado en la revisión de vacantes digitales y en el análisis documental de programas académicos vigentes. La cobertura curricular fue estimada mediante un Índice de Cobertura Curricular, complementado con una matriz de brechas por disciplina tecnológica. Los resultados sugieren baja presencia curricular en áreas como ingeniería de datos, DevOps e infraestructura cloud, en contraste con su presencia recurrente en vacantes tecnológicas. Se concluye que las instituciones de educación superior dominicanas requieren fortalecer mecanismos de actualización curricular basados en evidencia laboral verificable, articulación con empleadores y monitoreo continuo de tendencias tecnológicas.</pre>

<h3>7.2. Metodología corregida</h3>
<pre>La investigación adoptó un diseño descriptivo, transversal y comparativo. La unidad de análisis laboral estuvo constituida por vacantes tecnológicas publicadas en plataformas digitales de empleo durante el período enero–mayo de 2026. Se aplicaron criterios de inclusión relacionados con ubicación en República Dominicana, relación explícita con áreas STEAM y disponibilidad de descripción funcional del puesto. Se excluyeron vacantes duplicadas, publicaciones sin descripción suficiente y ofertas no vinculadas al territorio dominicano. La unidad de análisis curricular estuvo compuesta por programas de grado de nueve instituciones de educación superior seleccionadas por su participación en la formación tecnológica nacional. Las vacantes fueron clasificadas mediante una matriz de competencias emergentes, mientras que los programas académicos fueron codificados según el nivel de presencia curricular de cada disciplina. Para estimar la cobertura se calculó el Índice de Cobertura Curricular, definido como la proporción de instituciones que ofrecen una disciplina determinada. Se recomienda complementar este indicador con una escala ponderada que diferencie asignaturas aisladas, concentraciones, menciones y carreras completas.</pre>

<h3>7.3. Conclusiones corregidas</h3>
<pre>Los hallazgos sugieren la existencia de brechas relevantes entre ciertas competencias tecnológicas emergentes y la oferta curricular de grado examinada. En particular, las áreas de ingeniería de datos, DevOps, infraestructura cloud y automatización inteligente presentan baja representación curricular frente a su presencia en vacantes digitales. No obstante, debido al carácter transversal y descriptivo del estudio, estos resultados deben interpretarse como evidencia exploratoria y no como prueba causal. Se recomienda ampliar la investigación mediante análisis longitudinal de vacantes, entrevistas con empleadores, validación con expertos curriculares y publicación de bases de datos suplementarias que permitan replicar los resultados.</pre>
</section>

<section id="matriz" class="card">
<h2>8. Matriz correctiva</h2>
<table>
<tr><th>Problema</th><th>Impacto</th><th>Corrección</th><th>Texto sugerido</th></tr>
<tr><td>Uso de “descriptivo-causal”</td><td>Promete causalidad no demostrada</td><td>Cambiar a descriptivo-comparativo</td><td>“análisis descriptivo-comparativo...”</td></tr>
<tr><td>Porcentajes sin denominador</td><td>Reduce credibilidad de resultados</td><td>Reportar frecuencia absoluta y relativa</td><td>“La frecuencia fue calculada como n/N...”</td></tr>
<tr><td>Muestra no declarada</td><td>Impide replicación</td><td>Incluir N, filtros y criterios</td><td>“La muestra final estuvo compuesta por [N] vacantes únicas...”</td></tr>
<tr><td>ICC binario</td><td>Simplifica exceso de realidad curricular</td><td>Crear ICC ponderado</td><td>“0 = ausente; 1 = asignatura; 2 = concentración; 3 = carrera...”</td></tr>
<tr><td>Referencias no recuperables</td><td>Debilita trazabilidad</td><td>Agregar URL/DOI/repositorio</td><td>“Disponible en: [URL]. Recuperado el...”</td></tr>
<tr><td>Conclusiones categóricas</td><td>Sobreinterpretación</td><td>Usar lenguaje prudente</td><td>“Los hallazgos sugieren...”</td></tr>
</table>
</section>

<section id="rubrica" class="card">
<h2>9. Rúbrica de evaluación</h2>
<div class="score"><strong>Originalidad: 90/100</strong><div class="bar"><div class="fill" style="width:90%"></div></div></div>
<div class="score"><strong>Relevancia: 95/100</strong><div class="bar"><div class="fill" style="width:95%"></div></div></div>
<div class="score"><strong>Marco teórico: 78/100</strong><div class="bar"><div class="fill" style="width:78%"></div></div></div>
<div class="score"><strong>Metodología: 48/100</strong><div class="bar"><div class="fill" style="width:48%"></div></div></div>
<div class="score"><strong>Resultados: 58/100</strong><div class="bar"><div class="fill" style="width:58%"></div></div></div>
<div class="score"><strong>Discusión: 75/100</strong><div class="bar"><div class="fill" style="width:75%"></div></div></div>
<div class="score"><strong>Redacción científica: 84/100</strong><div class="bar"><div class="fill" style="width:84%"></div></div></div>
<div class="score"><strong>Referencias APA 7: 62/100</strong><div class="bar"><div class="fill" style="width:62%"></div></div></div>
</section>

<section id="plan" class="card">
<h2>10. Plan de mejora por fases</h2>
<div class="callout blue">
<h3>Fase 1: Corrección metodológica</h3>
<ul>
<li>Definir muestra final.</li>
<li>Publicar criterios de inclusión y exclusión.</li>
<li>Crear diccionario de codificación.</li>
<li>Validar clasificación con segundo evaluador.</li>
</ul>
</div>
<div class="callout blue">
<h3>Fase 2: Ajuste de resultados</h3>
<ul>
<li>Recalcular porcentajes con denominadores claros.</li>
<li>Convertir demanda proyectada en frecuencia observada o justificar modelo predictivo.</li>
<li>Agregar ICC ponderado.</li>
<li>Separar tendencias globales de evidencia local.</li>
</ul>
</div>
<div class="callout blue">
<h3>Fase 3: Reescritura</h3>
<ul>
<li>Moderar lenguaje causal.</li>
<li>Reestructurar resumen y conclusiones.</li>
<li>Auditar referencias APA 7.</li>
<li>Agregar anexo metodológico y base suplementaria.</li>
</ul>
</div>
</section>

<section id="veredicto" class="card">
<h2>11. Veredicto final</h2>
<div class="callout red">
<p><strong>Dictamen:</strong> REVISIÓN MAYOR.</p>
<p>El artículo no debe ser rechazado por su tema ni por su potencial, pero tampoco debe considerarse listo para publicación. Su contribución puede ser importante para la República Dominicana si transforma sus afirmaciones en evidencia replicable. La prioridad no es mejorar la redacción, sino fortalecer la base metodológica, documentar los datos, moderar la causalidad y hacer verificables las fuentes.</p>
</div>
</section>

</main>
</div>
</body>
</html>
