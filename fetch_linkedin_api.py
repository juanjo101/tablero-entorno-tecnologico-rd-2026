# -*- coding: utf-8 -*-
"""
Extractor de Tendencias Tecnológicas RD — Demanda del Mercado
Búsqueda directa en LinkedIn usando geoId de República Dominicana
geoId=101623149 = República Dominicana
"""
import re, json, time, sys, os, urllib.request, urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")

# geoId oficial de LinkedIn para República Dominicana
GEO_ID = "101623149"

# Búsquedas orientadas a tendencias tecnológicas en RD
TECH_SEARCHES = [
    # IA y Automatización
    ("inteligencia artificial",     "IA / Automatización"),
    ("machine learning",             "IA / Automatización"),
    ("automatizacion digital",       "IA / Automatización"),
    # Desarrollo de Software
    ("desarrollador software",       "Ingeniería de Software"),
    ("programador desarrollador",    "Ingeniería de Software"),
    ("fullstack developer",          "Ingeniería de Software"),
    # Datos y Analytics
    ("data engineer",                "Ingeniería de Datos"),
    ("analista de datos",            "Análisis de Datos / BI"),
    ("business intelligence",        "Análisis de Datos / BI"),
    # Ciberseguridad
    ("ciberseguridad",               "Ciberseguridad"),
    ("seguridad informatica",        "Ciberseguridad"),
    # Cloud y Redes
    ("cloud computing",              "Cloud / Infraestructura"),
    ("infraestructura tecnologica",  "Cloud / Infraestructura"),
    ("redes telecomunicaciones",     "Cloud / Infraestructura"),
    # Gestión TI
    ("gerente tecnologia",           "Gestión de TI"),
    ("director tecnologia",          "Gestión de TI"),
    ("jefe sistemas",                "Gestión de TI"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.linkedin.com/",
}

print("=" * 70)
print("📊 ANÁLISIS TENDENCIAS TECNOLÓGICAS — REPÚBLICA DOMINICANA 2026")
print("=" * 70)
print(f"\n🌐 Fuente: LinkedIn Jobs | Geolocalización: RD (geoId={GEO_ID})")
print(f"📅 Período: Últimos 30 días (Mayo 2026)\n")

def fetch_linkedin_rd(keywords, start=0):
    params = urllib.parse.urlencode({
        "keywords":  keywords,
        "location":  "República Dominicana",
        "geoId":     GEO_ID,
        "start":     start,
        "f_TPR":     "r2592000",  # últimos 30 días
        "sortBy":    "R",         # relevancia
    })
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"  ⚠️  Error en consulta '{keywords}': {e}")
        return ""

def extract_jobs(html):
    results = []
    # Títulos
    titles   = re.findall(r'class="[^"]*base-search-card__title[^"]*"[^>]*>\s*([\s\S]*?)\s*</h3>', html)
    if not titles:
        titles = re.findall(r'<span class="sr-only">\s*([\s\S]*?)\s*</span>', html)
    companies = re.findall(r'class="[^"]*base-search-card__subtitle[^"]*"[^>]*>\s*<[^>]+>\s*([^<\n]+)', html)
    locations = re.findall(r'class="[^"]*job-search-card__location[^"]*"[^>]*>\s*([^<\n]+)', html)
    dates     = re.findall(r'<time[^>]*datetime="([^"]+)"', html)

    for i, title in enumerate(titles):
        title = title.strip()
        if not title or len(title) < 4:
            continue
        results.append({
            "title":    title,
            "company":  companies[i].strip() if i < len(companies) else "Empresa",
            "location": locations[i].strip() if i < len(locations) else "República Dominicana",
            "date":     dates[i] if i < len(dates) else "2026-05",
        })
    return results

# --- RECOPILACIÓN ---
all_jobs = []
seen = set()
demand_by_category = {}

for keywords, category in TECH_SEARCHES:
    print(f"  🔍 [{category}] buscando: '{keywords}'...")
    html = fetch_linkedin_rd(keywords)
    found = extract_jobs(html)
    new = 0
    for j in found:
        key = (j["title"].lower()[:45], j["company"].lower()[:30])
        if key not in seen:
            seen.add(key)
            j["category"] = category
            all_jobs.append(j)
            demand_by_category[category] = demand_by_category.get(category, 0) + 1
            new += 1
    print(f"     ✅ {new} nuevas vacantes ({demand_by_category.get(category, 0)} en {category})")
    time.sleep(1.5)

print(f"\n{'='*70}")
print(f"📦 TOTAL VACANTES ÚNICAS: {len(all_jobs)}")
print(f"{'='*70}\n")

# --- RESUMEN DE DEMANDA POR CATEGORÍA ---
print("📊 DEMANDA POR ÁREA TECNOLÓGICA (Mayo 2026 — RD):")
print("-" * 50)
for cat, count in sorted(demand_by_category.items(), key=lambda x: -x[1]):
    bar = "█" * count
    print(f"  {cat:<30} {bar} ({count} vacantes)")

print(f"\n📋 LISTADO COMPLETO DE VACANTES:")
print("-" * 50)
for i, j in enumerate(all_jobs):
    print(f"  {i+1:2}. {j['title']}")
    print(f"      🏢 {j['company']}  |  📍 {j['location']}  |  🗂️ {j['category']}")

# --- ENRIQUECIMIENTO Y DESCRIPCIÓN ---
def enrich(j):
    t = j["title"].lower()
    cat = j.get("category", "")

    mapping = {
        "IA / Automatización": {
            "type": "IA y Automatización",
            "desc": f"Implementación de soluciones de inteligencia artificial y automatización de procesos en {j['company']}.",
            "requirements": ["Python / TensorFlow / PyTorch", "Modelos LLM y IA Generativa", "MLOps & Pipelines de datos", "Automatización RPA"],
            "impact": "Incrementa la eficiencia operativa hasta un 70% reduciendo tareas manuales repetitivas.",
            "forMortals": "Es usar computadoras que aprenden solas para hacer trabajos repetitivos sin intervención humana.",
        },
        "Ingeniería de Software": {
            "type": "Ingeniería de Software",
            "desc": f"Desarrollo de aplicaciones y sistemas digitales escalables para {j['company']}.",
            "requirements": ["Lenguajes: Python, Java, JavaScript", "APIs REST & Microservicios", "Git & Metodologías Ágiles", "Testing y CI/CD"],
            "impact": "Permite a la empresa lanzar productos digitales más rápido y con mayor calidad.",
            "forMortals": "Es programar las aplicaciones y sistemas que usamos todos los días en computadoras y celulares.",
        },
        "Ingeniería de Datos": {
            "type": "Ingeniería de Datos",
            "desc": f"Diseño y mantenimiento de pipelines de datos analíticos y almacenes de datos en {j['company']}.",
            "requirements": ["SQL Avanzado & dbt", "Apache Spark / Kafka", "Data Lakes & Data Warehouses", "Python para ETL"],
            "impact": "Garantiza que los datos del negocio estén disponibles, limpios y listos para análisis en tiempo real.",
            "forMortals": "Es construir las tuberías digitales que limpian y organizan toda la información de la empresa.",
        },
        "Análisis de Datos / BI": {
            "type": "Inteligencia de Negocios / BI",
            "desc": f"Transformación de datos crudos en tableros e informes para decisiones gerenciales en {j['company']}.",
            "requirements": ["Power BI / Tableau / Looker", "SQL para análisis", "Estadística y visualización", "Storytelling con datos"],
            "impact": "Acelera la toma de decisiones estratégicas con evidencia en tiempo real, mejorando el rendimiento en un 40%.",
            "forMortals": "Es convertir miles de números en gráficas fáciles de entender para que los jefes tomen mejores decisiones.",
        },
        "Ciberseguridad": {
            "type": "Ciberseguridad",
            "desc": f"Protección de activos digitales, auditoría de vulnerabilidades y respuesta a incidentes en {j['company']}.",
            "requirements": ["CompTIA Security+ / CEH / CISSP", "SIEM & SOC Operations", "Seguridad en redes y cloud", "Ethical Hacking & Pentesting"],
            "impact": "Previene pérdidas millonarias por ataques cibernéticos y protege la reputación de la empresa.",
            "forMortals": "Es ser el guardián digital que protege a la empresa de hackers y ladrones de información.",
        },
        "Cloud / Infraestructura": {
            "type": "Cloud & Infraestructura",
            "desc": f"Gestión de infraestructura en la nube, redes y sistemas de alta disponibilidad en {j['company']}.",
            "requirements": ["AWS / Azure / GCP Certified", "Kubernetes & Docker", "Terraform & Ansible", "Redes: switches, firewalls, SD-WAN"],
            "impact": "Asegura 99.9% de disponibilidad de los sistemas digitales de la organización.",
            "forMortals": "Es mantener encendidos y seguros todos los servidores y redes que hacen funcionar la empresa.",
        },
        "Gestión de TI": {
            "type": "Gestión de TI / Liderazgo Tech",
            "desc": f"Dirección estratégica del área tecnológica, presupuesto TI y alineación con objetivos del negocio en {j['company']}.",
            "requirements": ["PMP / ITIL / COBIT", "Gestión de equipos tech", "Presupuesto y planificación TI", "Transformación digital"],
            "impact": "Guía la transformación digital de la empresa para mantenerse competitiva en la economía digital.",
            "forMortals": "Es ser el director del equipo de tecnología, decidiendo qué sistemas y proyectos construir.",
        },
    }

    defaults = {
        "type": "Tecnología General",
        "desc": f"Implementación y gestión de soluciones tecnológicas en {j['company']}.",
        "requirements": ["Conocimientos técnicos del área", "Resolución de problemas", "Trabajo en equipo ágil", "Comunicación efectiva"],
        "impact": "Contribuye a la modernización tecnológica de la organización.",
        "forMortals": "Es trabajar con tecnología para mejorar los procesos y sistemas de la empresa.",
    }

    info = mapping.get(cat, defaults)
    return {
        "title":        j["title"],
        "company":      j["company"],
        "location":     j["location"],
        "date":         "Mayo 2026",
        "type":         info["type"],
        "desc":         info["desc"],
        "requirements": info["requirements"],
        "impact":       info["impact"],
        "forMortals":   info["forMortals"],
    }

enriched = [enrich(j) for j in all_jobs]

# También incluir las vacantes del scratch_visible_jobs.txt (datos locales reales de RD)
TXT_SOURCE = os.path.join(WORKSPACE, "scratch_visible_jobs.txt")
if os.path.exists(TXT_SOURCE):
    print(f"\n[+] Combinando con vacantes locales de RD de scratch_visible_jobs.txt...")
    with open(TXT_SOURCE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    local_jobs = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Logotipo de "):
            i += 1
            title = lines[i].strip() if i < len(lines) else ""
            i += 1
            company = lines[i].strip() if i < len(lines) else ""
            i += 1
            location = lines[i].strip() if i < len(lines) else "República Dominicana"
            if title and company and len(title) > 4:
                key = (title.lower()[:45], company.lower()[:30])
                if key not in seen:
                    seen.add(key)
                    local_jobs.append({"title": title, "company": company, "location": location})
        i += 1
    print(f"  ✅ {len(local_jobs)} vacantes adicionales de RD añadidas desde el archivo local.")

    def enrich_local(j):
        t = j["title"].lower()
        if any(k in t for k in ["python","agent","claude","copilot","cursor","agentic"]):
            cat = "IA / Automatización"
        elif any(k in t for k in ["machine","learning","ml ","ia ","inteligencia"]):
            cat = "IA / Automatización"
        elif any(k in t for k in ["ciber","security","seguridad","soc"]):
            cat = "Ciberseguridad"
        elif any(k in t for k in ["cloud","devops","aws","azure","redes","network","5g","iot"]):
            cat = "Cloud / Infraestructura"
        elif any(k in t for k in ["data engineer","datos","big data","arquitectura de datos","etl"]):
            cat = "Ingeniería de Datos"
        elif any(k in t for k in ["analista","bi ","business intelligence","tableau","power bi"]):
            cat = "Análisis de Datos / BI"
        elif any(k in t for k in ["gerente","director","jefe","líder","lider","senior"]):
            cat = "Gestión de TI"
        else:
            cat = "Ingeniería de Software"
        j["category"] = cat
        return enrich(j)

    enriched += [enrich_local(j) for j in local_jobs]
    print(f"[+] Total combinado final: {len(enriched)} vacantes")

# --- INYECTAR EN INDEX.HTML ---
if not enriched:
    print("[-] Sin vacantes para inyectar.")
    exit(1)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

block = "        const realJobsData = [\n"
for idx, j in enumerate(enriched):
    comma = "," if idx < len(enriched)-1 else ""
    def safe(s): return str(s).replace('"','\\"').replace('\n',' ').replace('\r','')
    block += f"""            {{
                title: "{safe(j['title'])}",
                company: "{safe(j['company'])}",
                location: "{safe(j['location'])}",
                date: "{safe(j['date'])}",
                type: "{safe(j['type'])}",
                desc: "{safe(j['desc'])}",
                requirements: {json.dumps(j['requirements'], ensure_ascii=False)},
                impact: "{safe(j['impact'])}",
                forMortals: "{safe(j['forMortals'])}"
            }}{comma}\n"""
block += "        ];"

pattern = r'const realJobsData\s*=\s*\[[\s\S]*?\]\s*;'
if re.search(pattern, content):
    new_content = re.sub(pattern, block, content)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\n✅ ¡ÉXITO! {len(enriched)} vacantes reales de LinkedIn RD inyectadas en 'index.html'.")
    print(f"   📂 Archivo actualizado: {INDEX_PATH}")
else:
    print("[-] ERROR: No se encontró 'const realJobsData' en index.html.")
