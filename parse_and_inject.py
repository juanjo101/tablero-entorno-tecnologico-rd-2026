# -*- coding: utf-8 -*-
import os
import re
import json

# Paths
WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
HTML_SOURCE = os.path.join(WORKSPACE, "empleos.html")

print("🚀 Iniciando automatizador de extracción e inyección de vacantes...")

if not os.path.exists(HTML_SOURCE):
    print(f"⚠️  ERROR: No se encontró el archivo '{HTML_SOURCE}'.")
    print("👉 Por favor, guarda la página de LinkedIn (Ctrl + S) con el nombre 'empleos.html' en la carpeta del proyecto y vuelve a correr este script.")
    exit(1)

with open(HTML_SOURCE, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Let's extract jobs from the saved HTML
# We can search for job titles, companies, locations, dates using Regex
# LinkedIn lists job cards with clean tags or json blobs in script tags.
# Let's extract any JSON payload or raw text patterns
jobs = []

# Pattern 1: Search inside translation lists or script payloads
# LinkedIn often dumps elements under collectionResponses
for block in re.finditer(r'\{"title":"([^"]+)","companyName":"([^"]+)","formattedLocation":"([^"]+)","postDate":"([^"]+)"', html_content):
    title, company, loc, date = block.groups()
    jobs.append({
        "title": title,
        "company": company,
        "location": loc,
        "date": date
    })

# Pattern 2: Fallback to HTML elements or text blocks
if not jobs:
    # Let's extract text-based structures from the HTML
    # Typically: Title, Company, Location, Date
    # Let's search using a general regex for common patterns
    matches = re.findall(r'Logotipo de ([^\n]+)\n([^\n]+)\n([^\n]+)\n([^\n\(\)]+)\(([^\)]+)\)', html_content)
    for m in matches:
        comp_logo, title, comp_name, loc, modality = m
        jobs.append({
            "title": title.strip(),
            "company": comp_name.strip(),
            "location": f"{loc.strip()} ({modality.strip()})",
            "date": "Hace poco"
        })

# Clean duplicates
unique_jobs = []
seen = set()
for j in jobs:
    key = (j["title"].lower(), j["company"].lower())
    if key not in seen:
        seen.add(key)
        unique_jobs.append(j)

print(f"📦 Se extrajeron {len(unique_jobs)} vacantes únicas del archivo.")

if not unique_jobs:
    print("⚠️  No se detectaron vacantes con los patrones estándar.")
    print("👉 Intentando extracción agresiva por palabras clave en los bloques de texto...")
    
    # Aggressive pattern matching
    # Search for lines like: Agentic Python Engineer, Cloud Architect, SOC Analyst, Network Engineer
    keywords = ["Engineer", "Developer", "Analista", "Gerente", "Specialist", "Manager", "Lead", "Consultor", "Supervisor"]
    lines = html_content.split('\n')
    for idx, line in enumerate(lines):
        line = line.strip()
        if any(k in line for k in keywords) and len(line) < 100:
            # Candidate job title
            # Let's see if the next lines contain company and location
            if idx + 1 < len(lines):
                next_line = lines[idx+1].strip()
                if len(next_line) > 1 and len(next_line) < 50:
                    company = next_line
                    location = "República Dominicana"
                    if idx + 2 < len(lines):
                        third_line = lines[idx+2].strip()
                        if "República Dominicana" in third_line or "Remoto" in third_line or "Presencial" in third_line or "Híbrido" in third_line:
                            location = third_line
                    
                    # Determine type
                    t_lower = line.lower()
                    j_type = "Tecnología"
                    if "python" in t_lower or "agent" in t_lower or "claude" in t_lower or "copilot" in t_lower:
                        j_type = "IA Agéntica"
                    elif "machine" in t_lower or "ml" in t_lower or "learning" in t_lower:
                        j_type = "Machine Learning"
                    elif "ciber" in t_lower or "security" in t_lower or "seguridad" in t_lower or "soc" in t_lower:
                        j_type = "Ciberseguridad"
                    elif "cloud" in t_lower or "devops" in t_lower or "aws" in t_lower or "azure" in t_lower:
                        j_type = "Tecnología Cloud / DevOps"
                    elif "data" in t_lower or "datos" in t_lower or "big" in t_lower:
                        j_type = "Ingeniería de Datos"
                    elif "bi" in t_lower or "intelligence" in t_lower or "negocios" in t_lower:
                        j_type = "Inteligencia de Negocios / BI"
                    elif "qa" in t_lower or "test" in t_lower or "pruebas" in t_lower:
                        j_type = "QA y Pruebas"
                    
                    unique_jobs.append({
                        "title": line,
                        "company": company,
                        "location": location,
                        "date": "Hace poco",
                        "type": j_type
                    })

    # Clean duplicates again
    final_jobs = []
    seen = set()
    for j in unique_jobs:
        key = (j["title"].lower(), j["company"].lower())
        if key not in seen and len(j["title"]) > 5 and len(j["company"]) > 2:
            seen.add(key)
            final_jobs.append(j)
    unique_jobs = final_jobs
    print(f"📦 Extracción agresiva completada. Total: {len(unique_jobs)} vacantes.")

if not unique_jobs:
    print("❌ No se pudieron extraer vacantes del archivo HTML. Asegúrate de haber guardado la página completa correctamente.")
    exit(1)

# Let's map detailed descriptions, requirements, impacts, forMortals to each extracted job dynamically
enriched_jobs = []
for j in unique_jobs:
    title = j["title"]
    company = j["company"]
    loc = j["location"]
    date = j.get("date", "Hace poco")
    j_type = j.get("type", "Tecnología")
    
    t_lower = title.lower()
    
    # Dynamic classification and detail generation
    if "python" in t_lower or "agent" in t_lower or "claude" in t_lower or "copilot" in t_lower or "cursor" in t_lower:
        j_type = "IA Agéntica"
        desc = f"Desarrollo e implementación de flujos autónomos y programación acelerada por IA en la infraestructura de {company}."
        reqs = ["Python / TypeScript", "Asistentes de IA (Cursor/Claude Code)", "Model Context Protocol", "LangGraph / CrewAI"]
        imp = "Aumenta la velocidad de desarrollo en un 60% automatizando tareas operativas repetitivas."
        mortals = "Es programar con la ayuda de asistentes de Inteligencia Artificial que escriben y corrigen código por ti."
    elif "machine" in t_lower or "learning" in t_lower or "ml" in t_lower:
        j_type = "Machine Learning / MLOps"
        desc = f"Diseño, entrenamiento e implementación de modelos de aprendizaje automático y visión computacional para {company}."
        reqs = ["Python (PyTorch, TensorFlow)", "MLOps & Pipelines", "Modelos de Lenguaje (LLMs)", "Procesamiento de Datos"]
        imp = "Habilita la toma de decisiones predictivas automáticas de alta fidelidad basada en datos históricos."
        mortals = "Es entrenar a las computadoras para que aprendan a predecir comportamientos o reconocer patrones solas."
    elif "ciber" in t_lower or "security" in t_lower or "seguridad" in t_lower or "soc" in t_lower:
        j_type = "Ciberseguridad"
        desc = f"Monitoreo de amenazas, auditoría de vulnerabilidades y defensa de perímetros digitales corporativos para {company}."
        reqs = ["CompTIA Security+ / CEH", "Detección de Intrusos (SIEM)", "Seguridad de Redes", "Ethical Hacking"]
        imp = "Protege el patrimonio digital corporativo y los datos de clientes ante ataques externos o malware."
        mortals = "Es como un guardia digital que vigila la red de la empresa para evitar hackeos o robos de información."
    elif "cloud" in t_lower or "devops" in t_lower or "aws" in t_lower or "azure" in t_lower or "telecom" in t_lower or "redes" in t_lower or "network" in t_lower or "5g" in t_lower or "iot" in t_lower:
        j_type = "Tecnología Cloud / Telecom"
        desc = f"Administración de infraestructuras de red, despliegues elásticos en la nube y conectividad de alta disponibilidad en {company}."
        reqs = ["Terraform / Ansible", "AWS / Azure Cloud Foundations", "Kubernetes & Docker", "Configuración de switches y firewalls"]
        imp = "Garantiza un tiempo de actividad del 99.9% para todas las plataformas digitales de la compañía."
        mortals = "Es estructurar y mantener los servidores de internet y la red para que los sistemas de la empresa nunca se caigan."
    elif "data" in t_lower or "datos" in t_lower or "big" in t_lower or "arquitectura" in t_lower or "foundry" in t_lower:
        j_type = "Ingeniería de Datos"
        desc = f"Construcción y optimización de almacenes de datos analíticos, flujos de extracción ETL y modelado dimensional en {company}."
        reqs = ["SQL Avanzado", "Apache Spark / dbt", "Data Lakes & Warehouses", "Python para ingeniería de datos"]
        imp = "Asegura que los datos de negocio estén siempre limpios, ordenados y listos para los analistas de negocio."
        mortals = "Es construir las 'tuberías digitales' que limpian y ordenan toda la información para que sea fácil analizarla."
    elif "bi" in t_lower or "intelligence" in t_lower or "negocios" in t_lower or "analista" in t_lower:
        j_type = "Inteligencia de Negocios / BI"
        desc = f"Transformación de datos crudos en informes y tableros interactivos para guiar las decisiones comerciales en {company}."
        reqs = ["Power BI / Tableau", "SQL para consultas", "Análisis de Requerimientos", "Estadística Comercial"]
        imp = "Acelera la toma de decisiones estratégicas basadas en evidencia empírica en un 40%."
        mortals = "Es tomar miles de números y convertirlos en gráficos de barras y pasteles interactivos muy fáciles de leer."
    elif "qa" in t_lower or "test" in t_lower or "pruebas" in t_lower:
        j_type = "QA y Pruebas"
        desc = f"Garantía de calidad de software y validación funcional automatizada de aplicaciones en {company}."
        reqs = ["Automatización de Pruebas (Selenium, Cypress)", "Casos de Prueba (QA Manual)", "Python / JavaScript básico", "Bug Tracking (Jira)"]
        imp = "Reduce el número de errores en producción y asegura que las aplicaciones funcionen perfectamente para el cliente."
        mortals = "Es el detective que se encarga de usar y probar las aplicaciones antes de que salgan al público para corregir fallos."
    else:
        j_type = "Ingeniería de Software"
        desc = f"Desarrollo e implementación de soluciones de software escalables y eficientes en {company}."
        reqs = ["Git / Metodologías Ágiles", "Diseño de APIs", "Frontend o Backend stack", "Resolución de Problemas"]
        imp = "Acelera el lanzamiento de nuevos productos y automatizaciones internas."
        mortals = "Es programar aplicaciones y sistemas modernos para resolver las necesidades del día a día de la empresa."

    enriched_jobs.append({
        "title": title,
        "company": company,
        "location": loc,
        "date": date,
        "type": j_type,
        "desc": desc,
        "requirements": reqs,
        "impact": imp,
        "forMortals": mortals
    })

# Now, let's load index.html, search for the realJobsData array, and replace it!
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Generate the javascript code block for the array
jobs_js_block = "        const realJobsData = [\n"
for idx, j in enumerate(enriched_jobs):
    comma = "," if idx < len(enriched_jobs) - 1 else ""
    jobs_js_block += f"""            {{
                title: "{j['title']}",
                company: "{j['company']}",
                location: "{j['location']}",
                date: "{j['date']}",
                type: "{j['type']}",
                desc: "{j['desc']}",
                requirements: {json.dumps(j['requirements'], ensure_ascii=False)},
                impact: "{j['impact']}",
                forMortals: "{j['forMortals']}"
            }}{comma}\n"""
jobs_js_block += "        ];"

# Find const realJobsData = [ ... ]; in index.html and replace it
pattern = r'const realJobsData\s*=\s*\[[\s\S]*?\]\s*;'
if re.search(pattern, index_content):
    new_index_content = re.sub(pattern, jobs_js_block, index_content)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_index_content)
    print("✅ ¡ÉXITO! Se inyectaron correctamente las nuevas vacantes en 'index.html'.")
else:
    print("❌ ERROR: No se encontró la declaración 'const realJobsData = [ ... ];' en 'index.html'.")
