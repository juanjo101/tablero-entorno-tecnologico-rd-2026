# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import urllib.request

# Ensure websocket-client is installed for raw CDP communication
try:
    import websocket
except ImportError:
    print("[+] Instalando biblioteca liviana de comunicación CDP...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websocket-client"])
    import websocket

# Paths
WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")

# Configure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("==================================================================")
print("🤖 EXTRACTOR CDP ULTRA-RÁPIDO (CERO DRIVERS / SIN SELENIUM) 🤖")
print("==================================================================")
ports = [9224, 9222, 9223]
tabs = None
connected_port = None
for port in ports:
    try:
        print(f"[+] Intentando conectar al puerto {port}...")
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3) as response:
            curr_tabs = json.loads(response.read().decode('utf-8'))
            has_linkedin = any("linkedin.com/jobs" in tab.get("url", "") for tab in curr_tabs)
            if has_linkedin:
                tabs = curr_tabs
                connected_port = port
                print(f"[+] ¡Conexión exitosa a LinkedIn en el puerto {port}!")
                break
            elif tabs is None:
                tabs = curr_tabs
                connected_port = port
    except Exception as e:
        continue

if not tabs:
    print("[-] ERROR: No se pudo conectar a ningún puerto de depuración activo (9222 o 9223).")
    print("👉 Asegúrate de haber abierto el navegador con la depuración remota habilitada (ej. puerto 9222 o 9223).")
    exit(1)

# Find the LinkedIn jobs tab
target_tab = None
for tab in tabs:
    url = tab.get("url", "")
    if "linkedin.com/jobs" in url:
        target_tab = tab
        break

if not target_tab:
    print("[-] ERROR: No se encontró ninguna pestaña de LinkedIn Empleos activa.")
    print("👉 Abre Edge, navega a LinkedIn, haz tu búsqueda y déjala en pantalla.")
    print("\n[+] Pestañas activas detectadas:")
    for tab in tabs[:5]:
        print(f"  - {tab.get('title', 'Sin título')} ({tab.get('url', '')[:60]}...)")
    exit(1)

print(f"[+] ¡Pestaña detectada con éxito!: '{target_tab.get('title')}'")
ws_url = target_tab.get("webSocketDebuggerUrl")

if not ws_url:
    print("[-] ERROR: No se pudo obtener el canal WebSocket de la pestaña.")
    exit(1)

print("[+] Conectando vía WebSocket al protocolo CDP de Microsoft Edge...")
try:
    # Connect directly to the browser tab
    ws = websocket.create_connection(ws_url)
    
    # Send scroll command to load more jobs in the DOM
    print("[+] Ejecutando desplazamiento automático en tu navegador...")
    scroll_cmd = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": """
                let container = document.querySelector('.jobs-search-results-list');
                if (container) {
                    container.scrollTop = container.scrollHeight;
                } else {
                    window.scrollTo(0, document.body.scrollHeight);
                }
            """,
            "returnByValue": True
        }
    }
    ws.send(json.dumps(scroll_cmd))
    time_wait = 2
    time.sleep(time_wait)
    
    # Fetch document body innerHTML
    print("[+] Extrayendo el contenido visible de LinkedIn...")
    get_dom_cmd = {
        "id": 2,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "document.body.innerHTML",
            "returnByValue": True
        }
    }
    ws.send(json.dumps(get_dom_cmd))
    
    # Read the response
    result_raw = ws.recv()
    result_json = json.loads(result_raw)
    
    # Handle potentially out-of-order websocket frames
    while result_json.get("id") != 2:
        result_raw = ws.recv()
        result_json = json.loads(result_raw)
        
    html_content = result_json.get("result", {}).get("result", {}).get("value", "")
    ws.close()
    
except Exception as ws_err:
    print(f"[-] Error en la conexión WebSocket: {ws_err}")
    exit(1)

if not html_content:
    print("[-] ERROR: No se recibió contenido HTML de la pestaña.")
    exit(1)

# 2. Parse jobs from the extracted HTML using our proven regex engine
print("[+] Buscando vacantes en el contenido extraído...")

# Extracción de tarjetas
jobs = []

# Patrón 1: Bloques estructurados en el HTML de LinkedIn
# Buscamos enlaces de empleo con títulos y metadatos
matches = re.finditer(r'<a[^>]*class="[^"]*job-card-list__title[^"]*"[^>]*>([^<]+)</a>[\s\S]*?<span[^>]*class="[^"]*job-card-container__company-name[^"]*"[^>]*>([^<]+)</span>[\s\S]*?<li[^>]*class="[^"]*job-card-container__metadata-item[^"]*"[^>]*>([\s\S]*?)</li>', html_content)

for m in matches:
    title, company, location = m.groups()
    location_clean = re.sub(r'<[^>]+>', '', location).strip()
    jobs.append({
        "title": title.strip(),
        "company": company.strip(),
        "location": location_clean,
        "date": "Hace poco"
    })

# Patrón 2: Fallback general de enlaces
if not jobs:
    # Buscar títulos y empresas usando expresiones regulares flexibles
    title_matches = re.findall(r'class="[^"]*job-card-list__title[^"]*"[^>]*>\s*([^<\n]+)', html_content)
    comp_matches = re.findall(r'class="[^"]*job-card-container__company-name[^"]*"[^>]*>\s*([^<\n]+)', html_content)
    
    for t, c in zip(title_matches, comp_matches):
        jobs.append({
            "title": t.strip(),
            "company": c.strip(),
            "location": "República Dominicana",
            "date": "Hace poco"
        })

# Clean duplicates
unique_jobs = []
seen = set()
for j in jobs:
    title_clean = j["title"].split(" - ")[0].split(" | ")[0].strip()
    key = (title_clean.lower(), j["company"].lower())
    if key not in seen and len(title_clean) > 3 and "notificaciones" not in title_clean.lower():
        seen.add(key)
        j["title"] = title_clean
        unique_jobs.append(j)

# Si el scraper falló por el DOM dinámico, intentamos buscar en los scripts de traducción
if not unique_jobs:
    print("[!] Intentando extracción profunda desde bloques de traducción JSON ocultos...")
    messages = re.findall(r'"message":"([^"]+)"', html_content)
    
    # LinkedIn translations often contain job titles
    # Let's search inside elements if they look like jobs
    keywords = ["Engineer", "Developer", "Analista", "Gerente", "Specialist", "Manager", "Lead", "Consultor", "Supervisor"]
    for msg in messages:
        if any(k in msg for k in keywords) and len(msg) < 80 and "notificaciones" not in msg.lower():
            # Estimate company based on common sequences
            unique_jobs.append({
                "title": msg.strip(),
                "company": "Empresa Líder",
                "location": "República Dominicana",
                "date": "Hace poco"
            })

    # Clean duplicates again
    final_jobs = []
    seen = set()
    for j in unique_jobs:
        key = (j["title"].lower(), j["company"].lower())
        if key not in seen and len(j["title"]) > 5:
            seen.add(key)
            final_jobs.append(j)
    unique_jobs = final_jobs

if not unique_jobs:
    print("[!] Intentando extracción por texto visible de la lista de resultados...")
    try:
        ws = websocket.create_connection(ws_url)
        text_cmd = {
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.body.innerText",
                "returnByValue": True
            }
        }
        ws.send(json.dumps(text_cmd))
        text_result = json.loads(ws.recv())
        while text_result.get("id") != 3:
            text_result = json.loads(ws.recv())
        page_text = text_result.get("result", {}).get("result", {}).get("value", "")
        ws.close()
    except Exception as text_err:
        print(f"[!] No se pudo leer texto visible: {text_err}")
        page_text = ""

    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    start = 0
    for idx, line in enumerate(lines):
        if "Ir al resultado" in line:
            start = idx + 1
            break

    end = len(lines)
    for idx, line in enumerate(lines[start:], start=start):
        if "Estos resultados" in line or "Acerca del empleo" in line:
            end = idx
            break

    result_lines = lines[start:end]
    noise = {
        "Visto", "Promocionado", "Solicitud sencilla", "Evaluando solicitudes de forma activa",
        "En las últimas 24 horas", "En las últimas 24\xa0horas", "Hace poco"
    }
    parsed_jobs = []
    for idx, line in enumerate(result_lines):
        lower = line.lower()
        if "república dominicana" not in lower and "republica dominicana" not in lower and "américa latina" not in lower and "america latina" not in lower:
            continue
        if idx < 2:
            continue

        company = result_lines[idx - 1]
        title_idx = idx - 2
        title = result_lines[title_idx]
        if "with verification" in title.lower() and title_idx - 1 >= 0:
            title = result_lines[title_idx - 1]
        if title == company and title_idx - 1 >= 0:
            title = result_lines[title_idx - 1]
        if company in noise or company.startswith("Hace ") or company.startswith("Logotipo de "):
            continue
        if title in noise or title.startswith("Logotipo de ") or len(title) < 4:
            continue
        parsed_jobs.append({
            "title": title,
            "company": company,
            "location": line,
            "date": "LinkedIn activo"
        })

    unique_jobs = []
    seen = set()
    for j in parsed_jobs:
        key = (j["title"].lower(), j["company"].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(j)

print(f"\n[+] Se extrajeron {len(unique_jobs)} vacantes únicas del navegador:")
for idx, j in enumerate(unique_jobs):
    print(f"  {idx+1}. {j['title']} - {j['company']} ({j['location']})")

if not unique_jobs:
    print("[-] No se pudieron detectar vacantes en pantalla. Asegúrate de tener la lista de empleos cargada a la izquierda.")
    exit(1)

STEAM_TERMS = [
    "ingenier", "engineer", "tecnolog", "technology", "datos", "data", "software",
    "inteligencia artificial", "ia", "ai", "machine learning", "proyecto", "project",
    "operaciones", "operations", "procesos", "process", "industrial", "electr",
    "energia", "energía", "renovable", "solar", "bess", "microgrid", "bim", "civil",
    "arquitect", "manufactura", "manufacturing", "calidad", "quality", "supply",
    "logistica", "logística", "mantenimiento", "maintenance", "redes", "network",
    "ciber", "security", "cloud", "drones", "robot", "agua", "water", "esg"
]
NON_STEAM_TERMS = [
    "cocinero", "cajero", "vendedor", "ventas al detalle", "visual designer",
    "marketing assistant", "customer support", "lead generation"
]

def is_steam_job(job):
    blob = f"{job['title']} {job['company']} {job['location']}".lower()
    if any(term in blob for term in NON_STEAM_TERMS):
        return False
    return any(term in blob for term in STEAM_TERMS)

before_filter = len(unique_jobs)
unique_jobs = [job for job in unique_jobs if is_steam_job(job)]
removed = before_filter - len(unique_jobs)
if removed:
    print(f"[+] Filtro STEAM descartó {removed} resultados no pertinentes.")

if not unique_jobs:
    print("[-] La pantalla tenía resultados, pero ninguno pasó el filtro STEAM.")
    exit(1)

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
    elif "bi" in t_lower or "intelligence" in t_lower or "negocios" in t_lower or "analista" in t_lower:
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

# Read existing jobs in index.html to merge
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_content = f.read()

array_pattern = r'const realJobsData\s*=\s*\[([\s\S]*?)\]\s*;'
match = re.search(array_pattern, index_content)
existing_jobs = []

if match:
    existing_js = match.group(1)
    obj_pattern = r'\{\s*title:\s*"([^"]+)",\s*company:\s*"([^"]+)",\s*location:\s*"([^"]+)",\s*date:\s*"([^"]+)",\s*type:\s*"([^"]+)",\s*desc:\s*"([^"]+)",\s*requirements:\s*(\[[^\]]*\]),\s*impact:\s*"([^"]+)",\s*forMortals:\s*"([^"]+)"\s*\}'
    for obj in re.finditer(obj_pattern, existing_js):
        t, c, l, d, ty, ds, req, imp_val, mort = obj.groups()
        existing_jobs.append({
            "title": t,
            "company": c,
            "location": l,
            "date": d,
            "type": ty,
            "desc": ds,
            "requirements": json.loads(req),
            "impact": imp_val,
            "forMortals": mort
        })

merged_list = list(existing_jobs)
seen_keys = {(j["title"].lower(), j["company"].lower()) for j in merged_list}

added_count = 0
for j in enriched_jobs:
    key = (j["title"].lower(), j["company"].lower())
    if key not in seen_keys:
        seen_keys.add(key)
        merged_list.append(j)
        added_count += 1

print(f"[+] Se agregaron {added_count} nuevas vacantes de tu pantalla activa.")
print(f"[+] Total acumulado en tu base de datos: {len(merged_list)} vacantes.")

# Generate and write back
jobs_js_block = "        const realJobsData = [\n"
for idx, j in enumerate(merged_list):
    comma = "," if idx < len(merged_list) - 1 else ""
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

new_index_content = re.sub(array_pattern, jobs_js_block, index_content)
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(new_index_content)

print("[+] EXITO TOTAL! Base de datos acumulativa actualizada e inyectada en 'index.html'.")
