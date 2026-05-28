# -*- coding: utf-8 -*-
"""
Validador de oferta de talento STEAM en LinkedIn RD.

Este script no guarda nombres, URLs ni datos personales. Solo captura conteos
agregados de resultados de busqueda de personas por habilidad/carrera y
ubicacion Republica Dominicana.

Uso:
    python linkedin_profiles_supply.py
    python linkedin_profiles_supply.py --inject
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
LATEST_JSON = os.path.join(WORKSPACE, "linkedin_profile_supply_latest.json")

GEO_URN_RD = "101623149"
LOCATION = "República Dominicana"

PROFILE_SEARCHES = [
    {"skill": "Ciberseguridad Zero Trust / SIEM", "keywords": "ciberseguridad OR cybersecurity OR SIEM OR SOC", "demand": 93},
    {"skill": "Cloud Engineering (AWS / Azure)", "keywords": "AWS OR Azure OR cloud engineer OR cloud computing", "demand": 94},
    {"skill": "DevOps / IaC (Terraform/K8s)", "keywords": "DevOps OR Terraform OR Kubernetes OR Infrastructure as Code", "demand": 91},
    {"skill": "IA Aplicada / LLMs / MLOps", "keywords": "inteligencia artificial OR machine learning OR MLOps OR LLM", "demand": 98},
    {"skill": "Prompt Engineering / IA Generativa", "keywords": "prompt engineering OR IA generativa OR generative AI OR ChatGPT", "demand": 85},
    {"skill": "Observability (Grafana/Prometheus)", "keywords": "Grafana OR Prometheus OR observability OR monitoring", "demand": 88},
    {"skill": "Inglés Técnico (B2-C1 real)", "keywords": "english B2 OR english C1 OR bilingual OR ingles tecnico", "demand": 95},
    {"skill": "Data Engineering / ETL Pipelines", "keywords": "data engineer OR ETL OR data pipeline OR Spark OR dbt", "demand": 82},
    {"skill": "RPA / Power Automate", "keywords": "RPA OR Power Automate OR UiPath OR automatizacion", "demand": 78},
    {"skill": "BIM / Revit / Construcción Digital", "keywords": "BIM OR Revit OR Navisworks OR construccion digital", "demand": 76},
    {"skill": "Automatización Industrial / PLC / SCADA", "keywords": "PLC OR SCADA OR instrumentacion industrial OR automatizacion industrial", "demand": 81},
    {"skill": "Manufactura Avanzada / Lean / Calidad", "keywords": "lean manufacturing OR calidad OR quality engineer OR manufactura", "demand": 74},
    {"skill": "Energía / Potencia / Eficiencia Energética", "keywords": "ingeniero electrico OR potencia OR eficiencia energetica OR energia", "demand": 72},
    {"skill": "Civil 3D / Gestión Digital de Obras", "keywords": "Civil 3D OR ingeniero civil OR gestion de obras OR construccion", "demand": 68},
    {"skill": "Energías Renovables / Solar FV / BESS", "keywords": "energia solar OR energias renovables OR fotovoltaica OR BESS", "demand": 88},
    {"skill": "Microrredes / Smart Grid / Gestión Energética", "keywords": "microgrid OR smart grid OR gestion energetica OR medicion inteligente", "demand": 77},
    {"skill": "Movilidad Eléctrica / Infraestructura de Carga", "keywords": "vehiculos electricos OR EV charging OR electromovilidad OR cargadores", "demand": 71},
    {"skill": "Drones / Robótica Móvil / Inspección Autónoma", "keywords": "drones OR robotica movil OR inspeccion autonoma OR fotogrametria", "demand": 69},
    {"skill": "Gestión Inteligente del Agua", "keywords": "gestion del agua OR tratamiento de agua OR drenaje OR hidraulica", "demand": 74},
    {"skill": "ESG / Carbono / Economía Circular", "keywords": "ESG OR carbono OR economia circular OR sostenibilidad", "demand": 67},
    {"skill": "Low-Code / Power Apps", "keywords": "Power Apps OR low code OR no code OR Power Platform", "demand": 75},
    {"skill": "Python Avanzado (ML/Data)", "keywords": "Python machine learning OR Python data OR Python developer", "demand": 80},
    {"skill": "Java / Spring Boot Empresarial", "keywords": "Java OR Spring Boot OR backend Java", "demand": 78},
    {"skill": "React / JavaScript Frontend", "keywords": "React OR JavaScript OR frontend developer", "demand": 70},
    {"skill": "SQL / Bases de Datos", "keywords": "SQL OR bases de datos OR database OR DBA", "demand": 72},
]


def linkedin_people_url(keywords):
    encoded_kw = urllib.parse.quote(keywords)
    encoded_geo = urllib.parse.quote(json.dumps([GEO_URN_RD]))
    return (
        "https://www.linkedin.com/search/results/people/"
        f"?keywords={encoded_kw}"
        f"&geoUrn={encoded_geo}"
        "&origin=GLOBAL_SEARCH_HEADER"
    )


def setup_driver():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError as exc:
        print(f"[x] Falta Selenium: {exc}")
        print("    Ejecuta: pip install selenium webdriver-manager")
        sys.exit(1)

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=es-419")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    })
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver, WebDriverWait, By


def wait_for_login(driver, WebDriverWait):
    print("\n[🔐] Abriendo LinkedIn Login...")
    driver.get("https://www.linkedin.com/login?lang=es")
    time.sleep(2)
    print("\nInicia sesion en Chrome. El script seguira cuando LinkedIn detecte la cuenta.\n")
    try:
        WebDriverWait(driver, 180).until(
            lambda d: (
                "linkedin.com/feed" in d.current_url
                or "linkedin.com/search" in d.current_url
                or "linkedin.com/in/" in d.current_url
                or "linkedin.com/mynetwork" in d.current_url
                or "linkedin.com/home" in d.current_url
            ) and "login" not in d.current_url
        )
        time.sleep(3)
        print("[✓] Sesion iniciada.")
    except Exception:
        print("[x] Tiempo agotado esperando login.")
        driver.quit()
        sys.exit(1)


def parse_count(text):
    normalized = text.replace("\xa0", " ")
    patterns = [
        r"(?:aproximadamente|cerca de|about)\s+([\d.,]+)\s+(?:resultados|results)",
        r"(?:mas de|más de|over)\s+([\d.,]+)\s+(?:resultados|results)",
        r"([\d.,]+)\s+(?:resultados|results)",
        r"([\d.,]+)\s+(?:persona|personas|people)",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if not match:
            continue
        raw = match.group(1)
        digits = re.sub(r"[^\d]", "", raw)
        if digits:
            return int(digits)
    return 0


def extract_result_count(driver, By):
    selectors = [
        "h2",
        ".search-results-container h2",
        ".pb2.t-black--light.t-14",
        ".search-results__total",
        "main",
        "body",
    ]
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                text = element.text.strip()
                count = parse_count(text)
                if count:
                    return count, text[:180]
        except Exception:
            continue
    return 0, ""


def classify_supply(count, max_count):
    if count <= 0 or max_count <= 0:
        return 0
    return max(1, min(100, round((count / max_count) * 100)))


def urgency_label(demand, supply):
    gap = demand - supply
    if gap >= 55:
        return "critical", "🔴 CRÍTICA"
    if gap >= 35:
        return "high", "🟠 ALTA"
    if gap >= 15:
        return "medium", "🟡 MEDIA"
    return "ok", "✅ CUBIERTA"


def collect_supply():
    driver, WebDriverWait, By = setup_driver()
    wait_for_login(driver, WebDriverWait)
    results = []

    print(f"\n[+] Validando oferta de perfiles LinkedIn en {LOCATION}")
    print("    Solo se guardan conteos agregados, no perfiles personales.\n")

    try:
        for idx, item in enumerate(PROFILE_SEARCHES, start=1):
            url = linkedin_people_url(item["keywords"])
            print(f"  [{idx:02}/{len(PROFILE_SEARCHES)}] {item['skill']}...")
            driver.get(url)
            time.sleep(6)
            count, evidence = extract_result_count(driver, By)
            results.append({
                "skill": item["skill"],
                "keywords": item["keywords"],
                "demand": item["demand"],
                "profileCount": count,
                "evidence": evidence,
                "url": url,
            })
            print(f"       perfiles agregados: {count}")
            time.sleep(2)
    finally:
        driver.quit()

    max_count = max([r["profileCount"] for r in results] or [0])
    for row in results:
        row["supply"] = classify_supply(row["profileCount"], max_count)
        row["urgency"], row["label"] = urgency_label(row["demand"], row["supply"])

    return results


def write_outputs(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    json_path = os.path.join(WORKSPACE, f"linkedin_profile_supply_{timestamp}.json")
    csv_path = os.path.join(WORKSPACE, f"linkedin_profile_supply_{timestamp}.csv")

    payload = {
        "source": "LinkedIn People Search",
        "location": LOCATION,
        "geoUrn": GEO_URN_RD,
        "capturedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "Conteo agregado por busqueda; no se guardan nombres, URLs ni perfiles individuales.",
        "results": results,
    }

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(LATEST_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["skill", "keywords", "demand", "profileCount", "supply", "urgency", "label", "url"],
        )
        writer.writeheader()
        for row in results:
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames})

    print(f"\n[✓] Resultados guardados:")
    print(f"    JSON: {json_path}")
    print(f"    CSV:  {csv_path}")
    print(f"    Latest: {LATEST_JSON}")


def inject_index(results):
    if not os.path.exists(INDEX_PATH):
        print(f"[x] No existe index.html en {INDEX_PATH}")
        return

    with open(INDEX_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()

    lookup = {row["skill"]: row for row in results}

    def update_item(match):
        raw = match.group(0)
        skill_match = re.search(r"skill:\s*'([^']+)'", raw)
        if not skill_match:
            return raw
        skill = skill_match.group(1)
        row = lookup.get(skill)
        if not row:
            return raw

        raw = re.sub(r"supply:\s*\d+", f"supply: {row['supply']}", raw)
        raw = re.sub(r"urgency:\s*'[^']+'", f"urgency: '{row['urgency']}'", raw)
        raw = re.sub(r"label:\s*'[^']+'", f"label: '{row['label']}'", raw)
        if "profileCount:" in raw:
            raw = re.sub(r"profileCount:\s*\d+", f"profileCount: {row['profileCount']}", raw)
        else:
            raw = raw.rstrip(" }") + f", profileCount: {row['profileCount']} }}"
        return raw

    pattern = r"\{\s*skill:\s*'[^']+'[\s\S]*?\}"
    new_content = re.sub(pattern, update_item, content)

    new_content = new_content.replace(
        "🔒 <strong>Fuentes de oferta:</strong> Auditoría de perfiles LinkedIn RD + BeBee + ENAE 2024 (Banco Central)",
        "🔒 <strong>Fuentes de oferta:</strong> Conteos agregados de LinkedIn People RD por habilidad/carrera + BeBee + ENAE 2024 (Banco Central)"
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        fh.write(new_content)

    print(f"[✓] index.html actualizado con supply validado por conteos agregados.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inject", action="store_true", help="Actualiza gapData en index.html con los conteos capturados.")
    parser.add_argument("--inject-latest", action="store_true", help="Actualiza index.html usando linkedin_profile_supply_latest.json sin volver a abrir LinkedIn.")
    args = parser.parse_args()

    print("=" * 70)
    print("VALIDADOR DE OFERTA LINKEDIN PEOPLE RD - CONTEOS AGREGADOS")
    print("=" * 70)

    if args.inject_latest:
        if not os.path.exists(LATEST_JSON):
            print(f"[x] No existe {LATEST_JSON}. Primero ejecuta: python linkedin_profiles_supply.py")
            sys.exit(1)
        with open(LATEST_JSON, "r", encoding="utf-8") as f:
            payload = json.load(f)
        inject_index(payload.get("results", []))
        return

    results = collect_supply()
    write_outputs(results)
    if args.inject:
        inject_index(results)

    print("\nResumen:")
    for row in sorted(results, key=lambda item: item["profileCount"], reverse=True):
        print(f"  {row['profileCount']:>6} perfiles | supply {row['supply']:>3}% | {row['skill']}")


if __name__ == "__main__":
    main()
