# -*- coding: utf-8 -*-
import os
import re
import json
import sys

# Ensure UTF-8 output even on older Windows shells
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paths
WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
TXT_SOURCE = os.path.join(WORKSPACE, "scratch_visible_jobs.txt")

print("[+] Iniciando el extractor de texto plano...")

if not os.path.exists(TXT_SOURCE):
    print("[-] ERROR: No se encontró scratch_visible_jobs.txt")
    exit(1)

with open(TXT_SOURCE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

jobs = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    
    # Check if this line is "Logotipo de ..."
    if line.startswith("Logotipo de "):
        company_logo = line.replace("Logotipo de ", "")
        
        # Next lines might contain Title, Company, Location
        title = ""
        company = ""
        location = ""
        
        # Advance index to inspect next items
        i += 1
        if i < len(lines):
            title = lines[i].strip()
        i += 1
        if i < len(lines):
            company = lines[i].strip()
        i += 1
        if i < len(lines):
            location = lines[i].strip()
            
        # Clean duplicates or noise
        if title and company and location and "notificaciones" not in title.lower():
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date": "Hace poco"
            })
    elif "Engineer" in line or "Developer" in line or "Analista" in line or "Gerente" in line or "Especialista" in line or "Specialist" in line or "QA" in line or "BIM" in line or "BHD" in line or "Popular" in line or "Drupal" in line:
        # Candidate standalone line
        title = line
        company = ""
        location = "República Dominicana"
        
        # Let's inspect around it
        if i + 1 < len(lines):
            company = lines[i+1].strip()
        if i + 2 < len(lines):
            location = lines[i+2].strip()
            
        if len(title) > 3 and len(company) > 1 and "notificaciones" not in title.lower() and "Logotipo" not in company:
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date": "Hace poco"
            })
            i += 2
    i += 1

# Clean duplicates
unique_jobs = []
seen = set()
for j in jobs:
    title_clean = j["title"].split(" - ")[0].split(" | ")[0].strip()
    key = (title_clean.lower(), j["company"].lower())
    if key not in seen and len(title_clean) > 3 and len(j["company"]) > 2:
        seen.add(key)
        j["title"] = title_clean
        unique_jobs.append(j)

print(f"[+] Se extrajeron {len(unique_jobs)} vacantes del texto plano:")
for idx, j in enumerate(unique_jobs):
    print(f"  {idx+1}. {j['title']} - {j['company']} ({j['location']})")

# Let's enrich them
enriched_jobs = []
for j in unique_jobs:
    title = j["title"]
    company = j["company"]
    loc = j["location"]
    date = j.get("date", "Hace poco")
    
    t_lower = title.lower()
    j_type = "Tecnología"
    desc = ""
    reqs = []
    imp = ""
    mortals = ""
    
    # Classification logic
    if "python" in t_lower or "agent" in t_lower or "claude" in t_lower or "copilot" in t_lower or "cursor" in t_lower:
        j_type = "IA Agéntica"
        desc = f"Desarrollo e implementación de flujos autónomos y programación acelerada por IA en {company}."
        reqs = ["Python / TypeScript", "Asistentes de IA (Cursor/Claude Code)", "Model Context Protocol", "LangGraph / CrewAI"]
        imp = "Aumenta la velocidad de desarrollo en un 60% automatizando tareas operativas repetitivas."
        mortals = "Es programar con la ayuda de asistentes de Inteligencia Artificial que escriben y corrigen código por ti."
    elif "machine" in t_lower or "learning" in t_lower or "ml" in t_lower:
        j_type = "Machine Learning"
        desc = f"Diseño, entrenamiento e implementación de modelos de aprendizaje automático y visión computacional en {company}."
        reqs = ["Python (PyTorch, TensorFlow)", "MLOps & Pipelines", "Modelos de Lenguaje (LLMs)", "Procesamiento de Datos"]
        imp = "Habilita la toma de decisiones predictivas automáticas de alta fidelidad basada en datos históricos."
        mortals = "Es entrenar a las computadoras para que aprendan a predecir comportamientos o reconocer patrones solas."
    elif "ciber" in t_lower or "security" in t_lower or "seguridad" in t_lower or "soc" in t_lower:
        j_type = "Ciberseguridad"
        desc = f"Monitoreo de amenazas, auditoría de vulnerabilidades y defensa de perímetros digitales corporativos en {company}."
        reqs = ["CompTIA Security+ / CEH", "Detección de Intrusos (SIEM)", "Seguridad de Redes", "Ethical Hacking"]
        imp = "Protege el patrimonio digital corporativo y los datos de clientes ante ataques externos o malware."
        mortals = "Es como un guardia digital que vigila la red de la empresa para evitar hackeos o robos de información."
    elif "cloud" in t_lower or "devops" in t_lower or "aws" in t_lower or "azure" in t_lower or "telecom" in t_lower or "redes" in t_lower or "network" in t_lower or "5g" in t_lower or "iot" in t_lower:
        j_type = "Tecnología Cloud / DevOps"
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
    elif "bi" in t_lower or "intelligence" in t_lower or "negocios" in t_lower or "analista" in t_lower or "planificador" in t_lower:
        j_type = "Inteligencia de Negocios / BI"
        desc = f"Transformación de datos crudos en informes y tableros interactivos para guiar las decisiones comerciales en {company}."
        reqs = ["Power BI / Tableau", "SQL para consultas", "Análisis de Requerimientos", "Estadística Comercial"]
        imp = "Acelera la toma de decisiones estratégicas basadas en evidencia empírica en un 40%."
        mortals = "Es tomar miles de números y convertirlos en gráficos de barras y pasteles interactivos muy fáciles de leer."
    elif "qa" in t_lower or "test" in t_lower or "pruebas" in t_lower or "calidad" in t_lower:
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

# Overwrite index.html with the new data!
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_content = f.read()

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

pattern = r'const realJobsData\s*=\s*\[[\s\S]*?\]\s*;'
if re.search(pattern, index_content):
    new_index_content = re.sub(pattern, jobs_js_block, index_content)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_index_content)
    print("[+] EXITO! Se inyectaron correctamente las nuevas vacantes reales en 'index.html'.")
else:
    print("[-] ERROR: No se encontró la declaración 'const realJobsData = [ ... ];' en 'index.html'.")
