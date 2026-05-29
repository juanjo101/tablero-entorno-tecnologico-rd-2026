# -*- coding: utf-8 -*-
"""
Pipeline salarial RD para el estudio STEAM.

Objetivo:
- Sector publico: agregar nomina publica MAP por cargo/categoria STEAM sin
  guardar nombres ni datos personales.
- Sector privado: extraer rangos publicados en vacantes cuando existan.
- Baseline: guardar pisos oficiales y promedios sectoriales documentados.

Ejemplos:
    python salary_pipeline_rd.py --write-baseline
    python salary_pipeline_rd.py --public-file nomina_map.csv
    python salary_pipeline_rd.py --private-jobs linkedin_jobs_demand_latest.csv
    python salary_pipeline_rd.py --download-map-csv
"""

import argparse
import csv
import io
import json
import os
import re
import statistics
import sys
import urllib.request
from datetime import datetime
from urllib.parse import urlparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WINDOWS_WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
WORKSPACE = WINDOWS_WORKSPACE if os.path.isdir(WINDOWS_WORKSPACE) else os.getcwd()
MAP_DATASET_ID = "nomina-publica-general-del-estado-2025-ministerio-de-administracion-publica-map"
CKAN_PACKAGE_URL = f"https://datos.gob.do/api/3/action/package_show?id={MAP_DATASET_ID}"

PUBLIC_OUTPUT_JSON = os.path.join(WORKSPACE, "salary_public_sector_latest.json")
PUBLIC_OUTPUT_CSV = os.path.join(WORKSPACE, "salary_public_sector_latest.csv")
PRIVATE_OUTPUT_JSON = os.path.join(WORKSPACE, "salary_private_jobs_latest.json")
PRIVATE_OUTPUT_CSV = os.path.join(WORKSPACE, "salary_private_jobs_latest.csv")
BASELINE_OUTPUT_JSON = os.path.join(WORKSPACE, "salary_reference_baseline.json")

ROLE_BUCKETS = [
    ("Ciberseguridad", ["ciber", "seguridad informatica", "security", "soc", "siem"]),
    ("Cloud / Infraestructura", ["cloud", "devops", "infraestructura", "redes", "network", "servidor", "soporte ti"]),
    ("IA / Automatización", ["inteligencia artificial", "machine learning", "automatizacion", "rpa", "python"]),
    ("Ingeniería de Datos / BI", ["data", "datos", "bi", "business intelligence", "base de datos", "sql", "reporting", "analyst", "power bi"]),
    ("Ingeniería de Software", ["software", "programador", "desarrollador", "developer", "sistemas", "ingeniero en sistemas", "aplicaciones"]),
    ("Ingeniería Electrónica", ["electronica", "electrónico", "instrumentacion", "plc", "scada", "iot"]),
    ("Ingeniería Eléctrica / Energía", ["electrica", "eléctrica", "energia", "energía", "potencia", "solar", "renovable"]),
    ("Ingeniería Mecánica / Movilidad", ["mecanica", "mecánica", "mantenimiento", "automotriz", "vehiculo", "vehículo"]),
    ("Ingeniería Industrial", ["industrial", "procesos", "operaciones", "logistica", "logística", "supply", "gerente operaciones"]),
    ("Manufactura / Calidad", ["manufactura", "calidad", "quality", "produccion", "producción", "lean", "sgc", "mejora continua"]),
    ("Ingeniería Civil / Infraestructura", ["civil", "obra", "construccion", "construcción", "infraestructura", "residente", "estructuras", "encargado de proyecto"]),
    ("Arquitectura / BIM", ["arquitect", "bim", "revit", "navisworks"]),
    ("ESG / Economía Circular", ["esg", "sostenibilidad", "ambiental", "carbono", "circular"]),
    ("Gestión de TI", ["gerente tecnologia", "gerente de ti", "director tecnologia", "encargado tecnologia"]),
]

BASELINE_SOURCES = {
    "capturedAt": datetime.now().isoformat(timespec="seconds"),
    "currency": "DOP",
    "minimumWagePrivate2026": [
        {
            "segment": "Sector privado no sectorizado - empresas grandes",
            "monthlySalary": 29988.00,
            "effectiveDate": "2026-02-01",
            "source": "EY, resumen Resolución CNS-01-2025",
            "url": "https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026",
        },
        {
            "segment": "Sector privado no sectorizado - empresas medianas",
            "monthlySalary": 27489.60,
            "effectiveDate": "2026-02-01",
            "source": "EY, resumen Resolución CNS-01-2025",
            "url": "https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026",
        },
        {
            "segment": "Sector privado no sectorizado - empresas pequeñas",
            "monthlySalary": 18421.20,
            "effectiveDate": "2026-02-01",
            "source": "EY, resumen Resolución CNS-01-2025",
            "url": "https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026",
        },
        {
            "segment": "Sector privado no sectorizado - microempresas",
            "monthlySalary": 16993.20,
            "effectiveDate": "2026-02-01",
            "source": "EY, resumen Resolución CNS-01-2025",
            "url": "https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026",
        },
        {
            "segment": "Zonas francas",
            "monthlySalary": 20875.00,
            "effectiveDate": "2026-06-01",
            "source": "EY, resumen Resolución CNS-03-2025",
            "url": "https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026",
        },
    ],
    "sectorAverages": [
        {
            "sector": "Comercio al por mayor y menor",
            "year": 2024,
            "monthlyAverageSalary": 28853.21,
            "source": "ONE, ENAE 2025 Sector Comercio",
            "url": "https://www.one.gob.do/media/rixbt34i/enae-2025-sector-comercio-al-por-mayor-y-al-por-menor.pdf",
        }
    ],
}


def normalize(text):
    value = str(text or "").lower()
    value = value.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    value = value.replace("ñ", "n")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_money(value):
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    cleaned = re.sub(r"[^\d,.\-]", "", raw)
    if not cleaned:
        return None
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        number = float(cleaned)
    except ValueError:
        return None
    return number if number > 0 else None


def classify_role(title):
    text = normalize(title)
    for bucket, keywords in ROLE_BUCKETS:
        if any(normalize(keyword) in text for keyword in keywords):
            return bucket
    return None


def percentile(values, pct):
    if not values:
        return None
    ordered = sorted(values)
    idx = (len(ordered) - 1) * pct
    lower = int(idx)
    upper = min(lower + 1, len(ordered) - 1)
    if lower == upper:
        return ordered[lower]
    weight = idx - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def summarize(groups):
    rows = []
    for role, values in sorted(groups.items()):
        clean = sorted(v for v in values if v is not None and v > 0)
        if not clean:
            continue
        rows.append({
            "role": role,
            "count": len(clean),
            "min": round(min(clean), 2),
            "p25": round(percentile(clean, 0.25), 2),
            "median": round(statistics.median(clean), 2),
            "average": round(statistics.mean(clean), 2),
            "p75": round(percentile(clean, 0.75), 2),
            "max": round(max(clean), 2),
        })
    return rows


def detect_columns(fieldnames):
    normalized = {normalize(name): name for name in fieldnames}
    title_candidates = ["cargo", "puesto", "funcion", "función", "posicion", "posición", "descripcion cargo"]
    salary_candidates = ["sueldo bruto", "suelto bruto", "salario bruto", "sueldo", "suelto", "salario", "remuneracion", "remuneración", "monto"]

    title_col = next((normalized[normalize(c)] for c in title_candidates if normalize(c) in normalized), None)
    salary_col = next((normalized[normalize(c)] for c in salary_candidates if normalize(c) in normalized), None)
    return title_col, salary_col


def read_csv_rows(path_or_text):
    if os.path.exists(path_or_text):
        with open(path_or_text, "r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t")
            return list(csv.DictReader(f, dialect=dialect))
    sample = path_or_text[:4096]
    dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t")
    return list(csv.DictReader(io.StringIO(path_or_text), dialect=dialect))


def aggregate_public_payroll(csv_path, source_label="MAP Nómina Pública"):
    rows = read_csv_rows(csv_path)
    if not rows:
        raise SystemExit("No hay filas en el archivo de nomina.")

    title_col, salary_col = detect_columns(rows[0].keys())
    if not title_col or not salary_col:
        available = ", ".join(rows[0].keys())
        raise SystemExit(f"No pude detectar columnas de cargo/salario. Columnas disponibles: {available}")

    groups = {}
    matched = 0
    for row in rows:
        role = classify_role(row.get(title_col))
        salary = parse_money(row.get(salary_col))
        if role and salary:
            groups.setdefault(role, []).append(salary)
            matched += 1

    summary = summarize(groups)
    payload = {
        "source": source_label,
        "capturedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "Agregacion por cargo desde nomina publica; no se guardan nombres ni registros individuales.",
        "titleColumn": title_col,
        "salaryColumn": salary_col,
        "matchedRows": matched,
        "results": summary,
    }
    write_salary_outputs(payload, PUBLIC_OUTPUT_JSON, PUBLIC_OUTPUT_CSV)
    return payload


def extract_salary_range(text):
    if not text:
        return None
    patterns = [
        r"(RD\$|DOP|US\$|USD)\s*([\d,.]+)\s*(?:-|a|–)\s*(?:RD\$|DOP|US\$|USD)?\s*([\d,.]+)",
        r"([\d,.]+)\s*(?:-|a|–)\s*([\d,.]+)\s*(RD\$|DOP|US\$|USD)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        parts = match.groups()
        currency = next((p.upper().replace("$", "") for p in parts if re.search(r"RD\$|DOP|US\$|USD", p, re.I)), "DOP")
        nums = [parse_money(p) for p in parts if parse_money(p)]
        if len(nums) >= 2:
            return {"currency": "USD" if currency == "US" else currency, "min": min(nums[:2]), "max": max(nums[:2])}
    return None


def aggregate_private_jobs(csv_path):
    rows = read_csv_rows(csv_path)
    groups = {}
    evidence_count = 0
    for row in rows:
        role = row.get("category") or row.get("type") or classify_role(row.get("title", ""))
        if row.get("salary_min") and row.get("salary_max"):
            currency = str(row.get("currency") or "DOP").upper()
            salary_min = parse_money(row.get("salary_min"))
            salary_max = parse_money(row.get("salary_max"))
            found = {"currency": currency, "min": salary_min, "max": salary_max}
        else:
            text = " ".join(str(row.get(key, "")) for key in row.keys())
            found = extract_salary_range(text)

        if role and role != "No clasificado" and found and found["currency"] in ("DOP", "RD") and found["min"] and found["max"]:
            monthly_midpoint = (found["min"] + found["max"]) / 2
            groups.setdefault(role, []).append(monthly_midpoint)
            evidence_count += 1

    summary = summarize(groups)
    payload = {
        "source": "Vacantes privadas con salario publicado",
        "capturedAt": datetime.now().isoformat(timespec="seconds"),
        "method": "Extraccion de rangos salariales explicitamente publicados en texto de vacantes; se usa el punto medio del rango.",
        "matchedRows": evidence_count,
        "results": summary,
    }
    write_salary_outputs(payload, PRIVATE_OUTPUT_JSON, PRIVATE_OUTPUT_CSV)
    return payload


def write_salary_outputs(payload, json_path, csv_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["role", "count", "min", "p25", "median", "average", "p75", "max"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload.get("results", []):
            writer.writerow(row)


def write_baseline():
    with open(BASELINE_OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(BASELINE_SOURCES, f, ensure_ascii=False, indent=2)
    print(f"[✓] Baseline salarial guardado: {BASELINE_OUTPUT_JSON}")


def latest_csv_resource(resources):
    csv_resources = [
        r for r in resources
        if str(r.get("format", "")).upper() == "CSV" or str(r.get("url", "")).lower().endswith(".csv")
    ]
    if not csv_resources:
        return None
    return csv_resources[-1]


def download_map_csv():
    with urllib.request.urlopen(CKAN_PACKAGE_URL, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    resource = latest_csv_resource(payload["result"]["resources"])
    if not resource:
        raise SystemExit("No encontre recurso CSV en datos.gob.do para la nomina MAP.")

    url = resource["url"]
    filename = os.path.basename(urlparse(url).path)
    if not filename or "." not in filename:
        filename = f"map_nomina_publica_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    path = os.path.join(WORKSPACE, filename)
    with urllib.request.urlopen(url, timeout=120) as response:
        content = response.read()
    with open(path, "wb") as f:
        f.write(content)
    print(f"[✓] CSV MAP descargado: {path}")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-baseline", action="store_true", help="Guarda pisos oficiales y promedios sectoriales documentados.")
    parser.add_argument("--public-file", help="CSV local de nomina publica para agregar rangos por categoria STEAM.")
    parser.add_argument("--download-map-csv", action="store_true", help="Descarga el ultimo CSV de Nomina Publica General MAP desde datos.gob.do.")
    parser.add_argument("--private-jobs", help="CSV de vacantes para extraer rangos salariales publicados.")
    args = parser.parse_args()

    if args.write_baseline:
        write_baseline()

    public_file = args.public_file
    if args.download_map_csv:
        public_file = download_map_csv()

    if public_file:
        payload = aggregate_public_payroll(public_file)
        print(f"[✓] Sector publico agregado: {payload['matchedRows']} filas coincidentes")
        print(f"    JSON: {PUBLIC_OUTPUT_JSON}")
        print(f"    CSV:  {PUBLIC_OUTPUT_CSV}")

    if args.private_jobs:
        payload = aggregate_private_jobs(args.private_jobs)
        print(f"[✓] Sector privado agregado: {payload['matchedRows']} vacantes con salario")
        print(f"    JSON: {PRIVATE_OUTPUT_JSON}")
        print(f"    CSV:  {PRIVATE_OUTPUT_CSV}")

    if not any([args.write_baseline, public_file, args.private_jobs]):
        parser.print_help()


if __name__ == "__main__":
    main()
