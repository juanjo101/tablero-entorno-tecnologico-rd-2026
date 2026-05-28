# -*- coding: utf-8 -*-
"""
🤖 EXTRACTOR LINKEDIN CON SELENIUM — TENDENCIAS TEC. RD 2026
=============================================================
1. Abre Chrome visible en tu pantalla
2. Espera que TÚ inicies sesión (credenciales privadas, no se guardan)
3. Hace búsquedas automáticas de empleos en República Dominicana
4. Extrae y clasifica vacantes por área tecnológica
5. Inyecta todo en index.html del tablero
"""

import sys
import os
import re
import csv
import json
import time
from datetime import datetime

# UTF-8 en consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
LATEST_DEMAND_JSON = os.path.join(WORKSPACE, "linkedin_jobs_demand_latest.json")
LATEST_DEMAND_CSV = os.path.join(WORKSPACE, "linkedin_jobs_demand_latest.csv")

print("=" * 65)
print("🚀 EXTRACTOR LINKEDIN SELENIUM — TENDENCIAS TEC. RD 2026")
print("=" * 65)

# ── Importar Selenium ─────────────────────────────────────────────
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    print("[✓] Selenium listo.")
except ImportError as e:
    print(f"[✗] Error importando Selenium: {e}")
    print("    Ejecuta: pip install selenium webdriver-manager")
    sys.exit(1)

# ── Configurar Chrome (visible, con tu perfil) ────────────────────
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--lang=es-419")
# NO guardar contraseñas
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.notifications": 2,
})
# No modo headless — abrimos ventana real para que veas todo
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

print("\n[+] Iniciando Chrome... (se abrirá en tu pantalla)")
try:
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
except Exception as e:
    print(f"[✗] No se pudo iniciar Chrome: {e}")
    sys.exit(1)

# ── Paso 1: Ir a LinkedIn e ESPERAR que el usuario inicie sesión ───
print("\n[🔐] Abriendo LinkedIn Login...")
driver.get("https://www.linkedin.com/login?lang=es")
time.sleep(2)

print("\n" + "=" * 65)
print("  ⏳ ESPERANDO QUE INICIES SESIÓN EN EL NAVEGADOR...")
print("  👉 Escribe tu correo y contraseña en la ventana de Chrome.")
print("  ✅ El script continúa automáticamente cuando LinkedIn")
print("     detecte que ya entraste a tu cuenta.")
print("=" * 65 + "\n")

# Esperar hasta 3 minutos a que la URL cambie a /feed o /jobs
try:
    WebDriverWait(driver, 180).until(
        lambda d: (
            "linkedin.com/feed" in d.current_url
            or "linkedin.com/jobs" in d.current_url
            or "linkedin.com/in/" in d.current_url
            or "linkedin.com/mynetwork" in d.current_url
            or "linkedin.com/home" in d.current_url
            or "linkedin.com/checkpoint/lg/login-submit" in d.current_url
        ) and "login" not in d.current_url
    )
    # esperar un segundo más por si redirige
    time.sleep(3)
    # Si quedó en checkpoint (verificación extra), esperar más
    if "checkpoint" in driver.current_url or "challenge" in driver.current_url:
        print("  ⚠️  LinkedIn pidió verificación adicional.")
        print("  👉 Completa la verificación en el navegador.")
        WebDriverWait(driver, 120).until(
            lambda d: "linkedin.com/feed" in d.current_url
                      or "linkedin.com/jobs" in d.current_url
        )
    print("[✓] ¡Sesión iniciada! Comenzando búsquedas...")
except Exception:
    print("[✗] Tiempo de espera agotado. ¿Iniciaste sesión?")
    driver.quit()
    sys.exit(1)

# ── Paso 2: Búsquedas de tendencias STEAM en RD ──────────────────
SEARCHES = [
    # Sistemas, datos e infraestructura
    ("inteligencia artificial",      "IA / Automatización"),
    ("machine learning",             "IA / Automatización"),
    ("desarrollador software",       "Ingeniería de Software"),
    ("fullstack developer",          "Ingeniería de Software"),
    ("data engineer",                "Ingeniería de Datos"),
    ("analista de datos",            "Análisis de Datos / BI"),
    ("business intelligence",        "Análisis de Datos / BI"),
    ("ciberseguridad",               "Ciberseguridad"),
    ("seguridad informatica",        "Ciberseguridad"),
    ("cloud computing",              "Cloud / Infraestructura"),
    ("devops",                       "Cloud / Infraestructura"),
    ("redes telecomunicaciones",     "Cloud / Infraestructura"),
    ("gerente tecnologia",           "Gestión de TI"),
    ("transformacion digital",       "Gestión de TI"),
    ("python developer",             "IA / Automatización"),
    ("network engineer",             "Cloud / Infraestructura"),
    # Electrónica, eléctrica y energía
    ("ingeniero electronico",        "Ingeniería Electrónica"),
    ("instrumentacion industrial",   "Ingeniería Electrónica"),
    ("PLC SCADA",                    "Ingeniería Electrónica"),
    ("IoT industrial",               "Ingeniería Electrónica"),
    ("ingeniero electrico",          "Ingeniería Eléctrica"),
    ("electrical engineer",          "Ingeniería Eléctrica"),
    ("energias renovables",          "Ingeniería Eléctrica"),
    ("energia solar",                "Ingeniería Eléctrica"),
    ("solar fotovoltaica",           "Ingeniería Eléctrica"),
    ("BESS",                         "Ingeniería Eléctrica"),
    ("microgrid",                    "Ingeniería Eléctrica"),
    ("smart grid",                   "Ingeniería Eléctrica"),
    ("vehiculos electricos",         "Ingeniería Eléctrica"),
    ("EV charging",                  "Ingeniería Eléctrica"),
    # Mecánica, robótica, manufactura e industrial
    ("ingeniero mecanico",           "Ingeniería Mecánica"),
    ("mechanical engineer",          "Ingeniería Mecánica"),
    ("mantenimiento predictivo",     "Ingeniería Mecánica"),
    ("vehiculos autonomos",          "Ingeniería Mecánica"),
    ("ADAS",                         "Ingeniería Mecánica"),
    ("robotica movil",               "Ingeniería Mecánica"),
    ("ingeniero industrial",         "Ingeniería Industrial"),
    ("industrial engineer",          "Ingeniería Industrial"),
    ("supply chain",                 "Ingeniería Industrial"),
    ("lean manufacturing",           "Ingeniería Industrial"),
    ("manufacturing engineer",       "Manufactura / Calidad"),
    ("ingeniero de calidad",         "Manufactura / Calidad"),
    ("mantenimiento industrial",     "Manufactura / Calidad"),
    ("drones inspeccion",            "Manufactura / Calidad"),
    ("materiales avanzados",         "Manufactura / Calidad"),
    # Civil, arquitectura, ambiente y ESG
    ("ingeniero civil",              "Ingeniería Civil"),
    ("civil engineer",               "Ingeniería Civil"),
    ("infraestructura civil",        "Ingeniería Civil"),
    ("gestion del agua",             "Ingeniería Civil"),
    ("drenaje urbano",               "Ingeniería Civil"),
    ("resiliencia climatica",        "Ingeniería Civil"),
    ("arquitecto",                   "Arquitectura / BIM"),
    ("BIM architect",                "Arquitectura / BIM"),
    ("BIM engineer",                 "Arquitectura / BIM"),
    ("revit BIM",                    "Arquitectura / BIM"),
    ("economia circular",            "ESG / Economía Circular"),
    ("ESG carbon",                   "ESG / Economía Circular"),
]

LOCATION = "República Dominicana"
all_jobs  = []
seen_keys = set()
demand_by_category = {}

def scroll_and_collect(driver):
    """Hace scroll en la lista de resultados para cargar más vacantes."""
    try:
        results_list = driver.find_elements(By.CSS_SELECTOR,
            ".jobs-search-results-list, .scaffold-layout__list, .jobs-search__results-list")
        if results_list:
            for _ in range(5):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_list[0])
                time.sleep(1.2)
        else:
            for _ in range(4):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.2)
    except:
        pass

def extract_jobs_from_page(driver, category):
    """
    Extrae tarjetas de empleo de la página actual.
    Estrategia: obtener el innerHTML completo vía JS y parsearlo con regex,
    ya que los selectores CSS del LinkedIn logueado cambian frecuentemente.
    """
    jobs_found = []
    time.sleep(3)
    scroll_and_collect(driver)
    time.sleep(1.5)

    # ── Estrategia 1: Selectores directos (logged-in UI) ──────────
    # LinkedIn logged-in usa estas clases en 2025-2026
    TITLE_SELECTORS = [
        ".job-card-list__title--link",
        ".job-card-list__title",
        ".jobs-unified-top-card__job-title a",
        "a.disabled.ember-view.job-card-list__title--link",
        "[data-test-app-aware-link]",
        ".artdeco-entity-lockup__title a",
        "strong",  # último recurso
    ]
    COMPANY_SELECTORS = [
        ".job-card-container__primary-description",
        ".job-card-container__company-name",
        ".artdeco-entity-lockup__subtitle span",
        ".job-card-fields__company-name",
    ]
    LOCATION_SELECTORS = [
        ".job-card-container__metadata-item",
        ".job-card-container__metadata-wrapper li",
        ".artdeco-entity-lockup__caption span",
        ".job-card-fields__work-location",
    ]

    try:
        titles_el   = driver.find_elements(By.CSS_SELECTOR, ", ".join(TITLE_SELECTORS[:4]))
        companies_el = driver.find_elements(By.CSS_SELECTOR, ", ".join(COMPANY_SELECTORS))
        locations_el = driver.find_elements(By.CSS_SELECTOR, ", ".join(LOCATION_SELECTORS))

        if titles_el:
            for i, t_el in enumerate(titles_el):
                title    = t_el.text.strip()
                company  = companies_el[i].text.strip() if i < len(companies_el) else "Empresa"
                location = locations_el[i].text.strip() if i < len(locations_el) else LOCATION
                if title and len(title) > 4 and "notificaciones" not in title.lower():
                    jobs_found.append({"title": title, "company": company,
                                       "location": location, "category": category})

            if jobs_found:
                return jobs_found
    except Exception:
        pass

    # ── Estrategia 2: JavaScript innerHTML + regex ─────────────────
    try:
        html = driver.execute_script("return document.body.innerHTML;")

        # Patrones para la UI de LinkedIn logueado (2025-2026)
        patterns = [
            # job-card con título, empresa y ubicación
            r'class="[^"]*job-card-list__title[^"]*"[^>]*>\s*<[^>]+>\s*([\w\s\-\/\(\)áéíóúñÁÉÍÓÚÑ,\.]+?)\s*<',
            # aria-label en links de trabajo
            r'aria-label="([^"]{5,80})"[^>]*class="[^"]*job-card[^"]*"',
            # títulos en elementos strong dentro de tarjetas
            r'class="[^"]*job-card[^"]*"[^>]*>[\s\S]{0,500}?<strong[^>]*>\s*([\w\s\-\/\(\)áéíóúñÁÉÍÓÚÑ,\.]+?)\s*</strong>',
        ]

        titles_raw   = []
        for pat in patterns:
            found = re.findall(pat, html)
            if found:
                titles_raw = found[:25]
                break

        companies_raw = re.findall(
            r'class="[^"]*(?:primary-description|company-name)[^"]*"[^>]*>\s*(?:<[^>]+>)?\s*([\w\s\-\.áéíóúñÁÉÍÓÚÑ&;]+?)\s*(?:<|$)',
            html)
        locations_raw = re.findall(
            r'class="[^"]*metadata-item[^"]*"[^>]*>\s*([\w\s\-\.,\(\)áéíóúñÁÉÍÓÚÑ]+?)\s*<',
            html)

        for i, title in enumerate(titles_raw):
            title = re.sub(r'\s+', ' ', title).strip()
            company  = companies_raw[i].strip() if i < len(companies_raw) else "Empresa"
            location = locations_raw[i].strip() if i < len(locations_raw) else LOCATION
            if title and len(title) > 4 and "notificaciones" not in title.lower():
                jobs_found.append({"title": title, "company": company,
                                   "location": location, "category": category})

        if jobs_found:
            return jobs_found
    except Exception as e:
        pass

    # ── Estrategia 3: Leer texto visible de la página ─────────────
    try:
        # Obtener todo el texto visible y buscar patrones de empleo
        page_text = driver.execute_script("""
            const results = [];
            const cards = document.querySelectorAll(
                '.job-card-container, .jobs-search-results__list-item, [data-job-id], li[class*="job"]'
            );
            cards.forEach(card => {
                results.push(card.innerText);
            });
            return results.join('|||CARD|||');
        """)

        if page_text:
            cards_text = page_text.split("|||CARD|||")
            for card_text in cards_text:
                lines = [l.strip() for l in card_text.strip().split('\n') if l.strip()]
                if len(lines) >= 2:
                    title   = lines[0]
                    company = lines[1] if len(lines) > 1 else "Empresa"
                    location = LOCATION
                    # buscar línea que parezca ubicación
                    for line in lines[2:5]:
                        if any(k in line for k in ["Dominicana", "Remoto", "Santo Domingo", "Híbrido", "Presencial"]):
                            location = line
                            break
                    if title and len(title) > 4 and len(title) < 120:
                        jobs_found.append({"title": title, "company": company,
                                           "location": location, "category": category})
    except Exception:
        pass

    return jobs_found


from selenium.webdriver.common.keys import Keys
import urllib.parse

def do_search(driver, keywords, location="República Dominicana"):
    """
    Realiza una búsqueda en LinkedIn Jobs usando la interfaz gráfica.
    Escribe la ubicación manualmente para que LinkedIn respete República Dominicana.
    """
    try:
        driver.get("https://www.linkedin.com/jobs/search/")
        time.sleep(3)

        kw_selectors = [
            "input[aria-label*='título']",
            "input[aria-label*='Search job']",
            "input[id*='jobs-search-box-keyword']",
            "input[name='keywords']",
            ".jobs-search-box__text-input[aria-label*='título']",
            ".jobs-search-box__text-input",
        ]
        kw_field = None
        for sel in kw_selectors:
            try:
                candidate = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if candidate.is_displayed():
                    kw_field = candidate
                    break
            except Exception:
                continue

        if kw_field:
            kw_field.click()
            kw_field.send_keys(Keys.CONTROL + "a")
            kw_field.send_keys(Keys.DELETE)
            time.sleep(0.3)
            kw_field.send_keys(keywords)
            time.sleep(0.5)

        loc_selectors = [
            "input[aria-label*='ubicación']",
            "input[aria-label*='City']",
            "input[aria-label*='Location']",
            "input[id*='jobs-search-box-location']",
            "input[name='location']",
            ".jobs-search-box__text-input[aria-label*='ubicación']",
        ]
        loc_field = None
        for sel in loc_selectors:
            try:
                candidate = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if candidate.is_displayed():
                    loc_field = candidate
                    break
            except Exception:
                continue

        if loc_field:
            loc_field.click()
            time.sleep(0.3)
            loc_field.send_keys(Keys.CONTROL + "a")
            loc_field.send_keys(Keys.DELETE)
            time.sleep(0.5)
            loc_field.send_keys(location)
            time.sleep(2)

            try:
                suggestion = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        ".basic-typeahead__selectable, .jobs-search-box__typeahead-item, [role='option']"
                    ))
                )
                suggestion.click()
                time.sleep(1)
            except Exception:
                loc_field.send_keys(Keys.RETURN)
                time.sleep(1)
        else:
            encoded_kw = urllib.parse.quote(keywords)
            fallback_url = (
                "https://www.linkedin.com/jobs/search/"
                f"?keywords={encoded_kw}"
                "&location=Rep%C3%BAblica+Dominicana"
                "&geoId=101623149"
                "&f_TPR=r2592000"
            )
            driver.get(fallback_url)
            time.sleep(3)
            return True

        try:
            search_btn = driver.find_element(
                By.CSS_SELECTOR,
                "button[type='submit'], .jobs-search-box__submit-button, button[data-tracking-control-name*='search']"
            )
            search_btn.click()
        except Exception:
            if loc_field:
                loc_field.send_keys(Keys.RETURN)

        time.sleep(4)
        return True

    except Exception as e:
        print(f"     ⚠️  Error en búsqueda UI: {e}")
        return False

print(f"\n{'─'*65}")
print(f"🔍 Iniciando {len(SEARCHES)} búsquedas de tendencias tecnológicas en RD")
print(f"{'─'*65}\n")

for keywords, category in SEARCHES:
    try:
        print(f"  🔍 [{category}] '{keywords}' en República Dominicana...")
        success = do_search(driver, keywords, "República Dominicana")
        if not success:
            print(f"     ⚠️  Búsqueda fallida, continuando...")
            continue

        found = extract_jobs_from_page(driver, category)
        new_count = 0
        for j in found:
            key = (j["title"].lower()[:45], j["company"].lower()[:30])
            if key not in seen_keys and len(j["title"]) > 4:
                seen_keys.add(key)
                j["date"] = "Mayo 2026"
                all_jobs.append(j)
                demand_by_category[category] = demand_by_category.get(category, 0) + 1
                new_count += 1

        print(f"     ✅ {new_count} nuevas vacantes  |  Total: {len(all_jobs)}")

    except Exception as e:
        print(f"     ⚠️  Error en '{keywords}': {e}")
    time.sleep(2)

driver.quit()
print(f"\n[✓] Navegador cerrado. Total vacantes únicas recopiladas: {len(all_jobs)}")


# ── Paso 3: Resumen de demanda por categoría ──────────────────────
print(f"\n{'='*65}")
print("📊 DEMANDA POR ÁREA TECNOLÓGICA — RD Mayo 2026")
print(f"{'─'*65}")
for cat, count in sorted(demand_by_category.items(), key=lambda x: -x[1]):
    bar = "█" * min(count, 30)
    print(f"  {cat:<35} {bar} ({count})")

# ── Paso 4: Enriquecer datos ──────────────────────────────────────
ENRICHMENT = {
    "IA / Automatización": {
        "type": "IA y Automatización",
        "desc": "Implementación de soluciones de inteligencia artificial y automatización de procesos operativos.",
        "requirements": ["Python / TensorFlow / PyTorch", "Modelos LLM y IA Generativa", "MLOps & Pipelines", "Automatización RPA"],
        "impact": "Incrementa la eficiencia operativa hasta un 70% reduciendo tareas manuales repetitivas.",
        "forMortals": "Es usar computadoras que aprenden solas para hacer trabajos repetitivos sin intervención humana.",
    },
    "Ingeniería de Software": {
        "type": "Ingeniería de Software",
        "desc": "Desarrollo de aplicaciones y sistemas digitales escalables para empresas dominicanas.",
        "requirements": ["Python, Java, JavaScript / TypeScript", "APIs REST & Microservicios", "Git & CI/CD", "Testing automatizado"],
        "impact": "Permite a las empresas lanzar productos digitales más rápido y con mayor calidad.",
        "forMortals": "Es programar las aplicaciones y sistemas que usamos todos los días en computadoras y celulares.",
    },
    "Ingeniería de Datos": {
        "type": "Ingeniería de Datos",
        "desc": "Diseño y mantenimiento de pipelines de datos analíticos y almacenes de datos.",
        "requirements": ["SQL Avanzado & dbt", "Apache Spark / Kafka", "Data Lakes & Warehouses", "Python para ETL"],
        "impact": "Garantiza que los datos del negocio estén disponibles, limpios y listos para análisis en tiempo real.",
        "forMortals": "Es construir las tuberías digitales que limpian y organizan toda la información de la empresa.",
    },
    "Análisis de Datos / BI": {
        "type": "Inteligencia de Negocios / BI",
        "desc": "Transformación de datos crudos en tableros e informes para decisiones gerenciales.",
        "requirements": ["Power BI / Tableau / Looker", "SQL para análisis", "Estadística y visualización", "Storytelling con datos"],
        "impact": "Acelera la toma de decisiones estratégicas con evidencia en tiempo real, mejorando resultados en un 40%.",
        "forMortals": "Es convertir miles de números en gráficas fáciles de entender para que los directivos tomen mejores decisiones.",
    },
    "Ciberseguridad": {
        "type": "Ciberseguridad",
        "desc": "Protección de activos digitales, auditoría de vulnerabilidades y respuesta a incidentes.",
        "requirements": ["CompTIA Security+ / CEH / CISSP", "SIEM & SOC Operations", "Seguridad en cloud y redes", "Ethical Hacking"],
        "impact": "Previene pérdidas millonarias por ataques cibernéticos y protege la reputación corporativa.",
        "forMortals": "Es ser el guardián digital que protege a la empresa de hackers y robos de información.",
    },
    "Cloud / Infraestructura": {
        "type": "Cloud & Infraestructura",
        "desc": "Gestión de infraestructura en la nube, redes y sistemas de alta disponibilidad.",
        "requirements": ["AWS / Azure / GCP Certified", "Kubernetes & Docker", "Terraform & Ansible", "Redes: switches, firewalls"],
        "impact": "Asegura 99.9% de disponibilidad de los sistemas digitales de la organización.",
        "forMortals": "Es mantener encendidos y seguros todos los servidores y redes que hacen funcionar la empresa.",
    },
    "Gestión de TI": {
        "type": "Gestión de TI / Liderazgo Tech",
        "desc": "Dirección estratégica del área tecnológica y alineación con los objetivos del negocio.",
        "requirements": ["PMP / ITIL / COBIT", "Gestión de equipos técnicos", "Presupuesto y planificación TI", "Transformación digital"],
        "impact": "Guía la transformación digital de la empresa para mantenerse competitiva en la economía digital.",
        "forMortals": "Es ser el director del equipo de tecnología, decidiendo qué sistemas y proyectos construir.",
    },
    "Ingeniería Electrónica": {
        "type": "Ingeniería Electrónica",
        "desc": "Diseño, diagnóstico e integración de sistemas electrónicos, instrumentación, PLC, SCADA e IoT industrial.",
        "requirements": ["PLC / SCADA", "Instrumentación industrial", "Sensores e IoT", "Electrónica de potencia"],
        "impact": "Mejora el monitoreo y control de procesos productivos críticos.",
        "forMortals": "Es conectar sensores, controles y equipos para que las máquinas puedan medirse, comunicarse y operar mejor.",
    },
    "Ingeniería Eléctrica": {
        "type": "Ingeniería Eléctrica / Energía",
        "desc": "Gestión de sistemas eléctricos, energía solar, renovables, BESS, microrredes, potencia y eficiencia energética.",
        "requirements": ["Sistemas de potencia", "Solar FV / BESS", "Smart Grid / Microgrid", "Normativas eléctricas"],
        "impact": "Reduce costos energéticos y mejora la continuidad de infraestructura crítica.",
        "forMortals": "Es diseñar y operar energía segura, eficiente y cada vez más renovable para empresas y comunidades.",
    },
    "Ingeniería Mecánica": {
        "type": "Ingeniería Mecánica / Movilidad",
        "desc": "Mantenimiento predictivo, sistemas mecánicos, robótica móvil, vehículos eléctricos o autónomos y soporte a producción.",
        "requirements": ["Mantenimiento predictivo", "CAD / diseño mecánico", "Robótica / ADAS", "Análisis de fallas"],
        "impact": "Reduce paradas de equipos y habilita nuevas soluciones de movilidad e inspección.",
        "forMortals": "Es mantener y mejorar máquinas, vehículos y equipos para que trabajen con menos fallas y más inteligencia.",
    },
    "Ingeniería Industrial": {
        "type": "Ingeniería Industrial",
        "desc": "Optimización de procesos, logística, supply chain, mejora continua, calidad, productividad y analítica operacional.",
        "requirements": ["Lean Six Sigma", "Supply Chain", "Power BI / Excel avanzado", "Gestión de procesos"],
        "impact": "Reduce desperdicio, tiempos y costos operativos mediante procesos mejor diseñados.",
        "forMortals": "Es ordenar cómo trabaja una empresa para producir más, gastar menos y cometer menos errores.",
    },
    "Ingeniería Civil": {
        "type": "Ingeniería Civil / Agua e Infraestructura",
        "desc": "Diseño, supervisión y gestión de infraestructura civil, drenaje, agua, resiliencia climática y obras.",
        "requirements": ["Civil 3D / AutoCAD", "Gestión de obras", "Drenaje y agua", "Resiliencia climática"],
        "impact": "Permite desarrollar infraestructura más segura, sostenible y resistente al clima.",
        "forMortals": "Es diseñar y supervisar obras, agua y drenaje para que funcionen bien y resistan el uso y el clima.",
    },
    "Arquitectura / BIM": {
        "type": "Arquitectura / BIM",
        "desc": "Diseño arquitectónico, coordinación BIM, documentación digital, modelos 3D y gemelos digitales de construcción.",
        "requirements": ["Revit / BIM", "Navisworks", "Coordinación multidisciplinaria", "Visualización 3D"],
        "impact": "Reduce errores de diseño y mejora la coordinación entre arquitectura, ingeniería y construcción.",
        "forMortals": "Es construir el edificio primero en un modelo digital para encontrar errores antes de gastar en obra.",
    },
    "Manufactura / Calidad": {
        "type": "Manufactura / Calidad",
        "desc": "Mejora de manufactura, calidad, mantenimiento industrial, dispositivos médicos, trazabilidad y control estadístico.",
        "requirements": ["Lean Manufacturing", "ISO / GMP", "Control estadístico", "Validación de procesos"],
        "impact": "Eleva la calidad del producto y reduce fallas, retrabajos y desperdicios en planta.",
        "forMortals": "Es mejorar cómo se fabrica un producto para que salga bien, seguro y con menos defectos.",
    },
    "ESG / Economía Circular": {
        "type": "ESG / Carbono / Economía Circular",
        "desc": "Medición de huella de carbono, eficiencia de recursos, reportes ESG, circularidad y reducción de residuos.",
        "requirements": ["ESG", "Huella de carbono", "Economía circular", "Gestión ambiental"],
        "impact": "Ayuda a cumplir estándares ambientales y a reducir costos por energía, residuos y materiales.",
        "forMortals": "Es medir y reducir el impacto ambiental de una operación para producir con menos desperdicio.",
    },
}

DEFAULT_ENRICHMENT = {
    "type": "Tecnología General",
    "desc": "Implementación y gestión de soluciones tecnológicas en empresas dominicanas.",
    "requirements": ["Conocimientos técnicos del área", "Resolución de problemas", "Metodologías ágiles", "Comunicación efectiva"],
    "impact": "Contribuye a la modernización tecnológica y transformación digital de la organización.",
    "forMortals": "Es trabajar con tecnología para mejorar los procesos y sistemas de la empresa.",
}

def safe(s):
    return str(s).replace('"', '\\"').replace('\n', ' ').replace('\r', '')

def infer_category(title):
    t = title.lower()
    if any(k in t for k in ["bim", "arquitect", "revit"]):
        return "Arquitectura / BIM"
    if any(k in t for k in ["electrical", "eléctr", "electric", "solar", "renovable", "bess", "microgrid", "smart grid", "energia", "energía", "ev charging"]):
        return "Ingeniería Eléctrica"
    if any(k in t for k in ["electron", "instrumentacion", "instrumentación", "plc", "scada", "iot"]):
        return "Ingeniería Electrónica"
    if any(k in t for k in ["mechanical", "mecánico", "mecanico", "predictivo", "autonom", "adas", "robotica", "robótica"]):
        return "Ingeniería Mecánica"
    if any(k in t for k in ["industrial", "logística", "logistica", "supply", "process", "procesos", "operaciones", "lean"]):
        return "Ingeniería Industrial"
    if any(k in t for k in ["civil", "obra", "drenaje", "agua", "resiliencia", "infraestructura"]):
        return "Ingeniería Civil"
    if any(k in t for k in ["manufacturing", "manufactura", "mfg", "quality", "calidad", "producción", "produccion", "mantenimiento", "maintenance", "drones", "materiales"]):
        return "Manufactura / Calidad"
    if any(k in t for k in ["esg", "carbon", "circular"]):
        return "ESG / Economía Circular"
    if any(k in t for k in ["python", "agent", "claude", "copilot", "ia", "inteligencia", "machine", "learning"]):
        return "IA / Automatización"
    if any(k in t for k in ["ciber", "security", "seguridad"]):
        return "Ciberseguridad"
    if any(k in t for k in ["cloud", "devops", "aws", "azure", "redes", "network"]):
        return "Cloud / Infraestructura"
    if any(k in t for k in ["data engineer", "datos", "arquitectura de datos"]):
        return "Ingeniería de Datos"
    if any(k in t for k in ["analista", "bi ", "business", "power bi"]):
        return "Análisis de Datos / BI"
    if any(k in t for k in ["gerente", "director", "lider", "líder"]):
        return "Gestión de TI"
    return "Ingeniería de Software"

enriched = []
for j in all_jobs:
    info = ENRICHMENT.get(j.get("category", ""), DEFAULT_ENRICHMENT)
    enriched.append({
        "title":        j["title"],
        "company":      j["company"],
        "location":     j["location"],
        "date":         j.get("date", "Mayo 2026"),
        "type":         info["type"],
        "desc":         f"{info['desc'].rstrip('.')} en {j['company']}.",
        "requirements": info["requirements"],
        "impact":       info["impact"],
        "forMortals":   info["forMortals"],
    })

# Combinar con datos locales de RD de scratch_visible_jobs.txt
TXT = os.path.join(WORKSPACE, "scratch_visible_jobs.txt")
if os.path.exists(TXT):
    print(f"\n[+] Añadiendo vacantes locales de RD desde scratch_visible_jobs.txt...")
    with open(TXT, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    i = 0
    local_added = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Logotipo de "):
            i += 1
            title   = lines[i].strip() if i < len(lines) else ""
            i += 1
            company = lines[i].strip() if i < len(lines) else ""
            i += 1
            loc     = lines[i].strip() if i < len(lines) else "República Dominicana"
            if title and company and len(title) > 4:
                key = (title.lower()[:45], company.lower()[:30])
                if key not in seen_keys:
                    seen_keys.add(key)
                    cat = infer_category(title)
                    info = ENRICHMENT.get(cat, DEFAULT_ENRICHMENT)
                    enriched.append({
                        "title":        title,
                        "company":      company,
                        "location":     loc,
                        "date":         "Mayo 2026",
                        "type":         info["type"],
                        "desc":         f"{info['desc'].rstrip('.')} en {company}.",
                        "requirements": info["requirements"],
                        "impact":       info["impact"],
                        "forMortals":   info["forMortals"],
                    })
                    local_added += 1
        i += 1
    print(f"  ✅ {local_added} vacantes adicionales de RD añadidas.")

print(f"\n[+] Total final de vacantes a inyectar: {len(enriched)}")

def write_demand_outputs(jobs, demand_summary):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    json_path = os.path.join(WORKSPACE, f"linkedin_jobs_demand_{timestamp}.json")
    csv_path = os.path.join(WORKSPACE, f"linkedin_jobs_demand_{timestamp}.csv")
    captured_at = datetime.now().isoformat(timespec="seconds")

    payload = {
        "source": "LinkedIn Jobs",
        "location": LOCATION,
        "capturedAt": captured_at,
        "method": "Vacantes activas capturadas por busquedas tematicas STEAM en LinkedIn Jobs; se deduplican por titulo y empresa.",
        "searches": [{"keywords": keywords, "category": category} for keywords, category in SEARCHES],
        "totalJobs": len(jobs),
        "demandByCategory": demand_summary,
        "jobs": jobs,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(LATEST_DEMAND_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    fields = ["title", "company", "location", "date", "type", "desc", "requirements", "impact", "forMortals"]
    for path in (csv_path, LATEST_DEMAND_CSV):
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for job in jobs:
                row = dict(job)
                row["requirements"] = " | ".join(job.get("requirements", []))
                writer.writerow(row)

    print("[✓] Evidencia de demanda guardada:")
    print(f"   • JSON: {json_path}")
    print(f"   • CSV:  {csv_path}")
    print(f"   • Latest JSON: {LATEST_DEMAND_JSON}")
    print(f"   • Latest CSV:  {LATEST_DEMAND_CSV}")

write_demand_outputs(enriched, demand_by_category)

# ── Paso 5: Inyectar en index.html ────────────────────────────────
if not enriched:
    print("[✗] No hay vacantes para inyectar.")
    sys.exit(1)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

block = "        const realJobsData = [\n"
for idx, j in enumerate(enriched):
    comma = "," if idx < len(enriched) - 1 else ""
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
    print(f"\n{'='*65}")
    print(f"✅ ¡ÉXITO TOTAL!")
    print(f"   • {len(enriched)} vacantes reales de LinkedIn RD inyectadas")
    print(f"   • Archivo actualizado: {INDEX_PATH}")
    print(f"{'='*65}")
else:
    print("[✗] ERROR: No se encontró 'const realJobsData' en index.html.")
