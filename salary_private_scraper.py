# -*- coding: utf-8 -*-
"""
Recolector de salarios privados publicados en portales de empleo RD.

El objetivo no es descargar perfiles ni datos personales. Solo se guardan
vacantes donde el portal publica un rango o monto salarial visible.

Uso recomendado:
    python salary_private_scraper.py --source computrabajo --limit 3
    python salary_private_scraper.py --all --limit 2
    python salary_private_scraper.py --html-dir muestras_portales

Luego agregar rangos:
    python salary_pipeline_rd.py --private-jobs salary_private_raw_latest.csv
"""

import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WINDOWS_WORKSPACE = r"C:\Users\jdiaz\Documents\antigravity\resilient-planck"
WORKSPACE = WINDOWS_WORKSPACE if os.path.isdir(WINDOWS_WORKSPACE) else os.getcwd()

RAW_CSV = os.path.join(WORKSPACE, "salary_private_raw_latest.csv")
RAW_JSON = os.path.join(WORKSPACE, "salary_private_raw_latest.json")

SEARCH_TERMS = [
    "desarrollador software",
    "data engineer",
    "ciberseguridad",
    "cloud engineer",
    "devops",
    "ingeniero electrico",
    "energia solar",
    "ingeniero mecanico",
    "ingeniero industrial",
    "ingeniero civil",
    "arquitecto revit",
    "BIM",
    "PLC SCADA",
    "ingeniero de calidad",
    "manufacturing engineer",
    "sostenibilidad ESG",
]

SOURCES = {
    "computrabajo": {
        "name": "Computrabajo RD",
        "url": "https://do.computrabajo.com/ofertas-de-trabajo/?q={query}",
    },
    "tecoloco": {
        "name": "Tecoloco RD",
        "url": "https://www.tecoloco.com.do/trabajo?q={query}",
    },
    "tuempleord": {
        "name": "Tu Empleo RD",
        "url": "https://tuempleord.do/buscar?keyword={query}",
    },
    "rdtrabaja": {
        "name": "RD Trabaja",
        "url": "https://rdtrabaja.mt.gob.do/Home/Opcionesempleos?buscar={query}",
    },
    "jooble": {
        "name": "Jooble RD",
        "url": "https://do.jooble.org/SearchResult?k={query}&l=Rep%C3%BAblica%20Dominicana",
    },
    "buscojobs": {
        "name": "BuscoJobs RD",
        "url": "https://www.buscojobs.com.do/trabajos?Search={query}",
    },
    "computrabajo_it": {
        "name": "Computrabajo RD - Informática",
        "url": "https://do.computrabajo.com/empleos-de-informatica-y-telecom",
    },
    "computrabajo_engineering": {
        "name": "Computrabajo RD - Ingeniería",
        "url": "https://do.computrabajo.com/empleos-de-ingenieria-y-tecnico",
    },
}

ROLE_BUCKETS = [
    ("Ciberseguridad", ["ciber", "cyber", "seguridad informatica", "security", "soc", "siem"]),
    ("Cloud / Infraestructura", ["cloud", "devops", "infraestructura", "redes", "network", "servidor"]),
    ("IA / Automatización", ["inteligencia artificial", "machine learning", "automatizacion", "rpa", "python"]),
    ("Ingeniería de Datos / BI", ["data", "datos", "bi", "business intelligence", "sql", "etl", "reporting", "analyst", "power bi"]),
    ("Ingeniería de Software", ["software", "programador", "desarrollador", "developer", "frontend", "backend", "fullstack", "ingeniero en sistemas", "sistemas"]),
    ("Ingeniería Electrónica", ["electronica", "electronico", "instrumentacion", "plc", "scada", "iot"]),
    ("Ingeniería Eléctrica / Energía", ["electrica", "electrico", "energia", "solar", "renovable", "potencia"]),
    ("Ingeniería Mecánica / Movilidad", ["mecanica", "mecanico", "mantenimiento", "automotriz", "vehiculo"]),
    ("Ingeniería Industrial", ["industrial", "procesos", "operaciones", "logistica", "supply", "gerente operaciones"]),
    ("Manufactura / Calidad", ["manufactura", "calidad", "quality", "produccion", "lean", "sgc", "mejora continua"]),
    ("Ingeniería Civil / Infraestructura", ["civil", "obra", "construccion", "infraestructura", "residente", "estructuras", "encargado de proyecto"]),
    ("Arquitectura / BIM", ["arquitect", "bim", "revit", "navisworks"]),
    ("ESG / Economía Circular", ["esg", "sostenibilidad", "ambiental", "carbono", "circular"]),
]


def normalize(text):
    value = str(text or "").lower()
    value = value.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    value = value.replace("ñ", "n")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def classify_role(title):
    text = normalize(title)
    for bucket, keywords in ROLE_BUCKETS:
        if any(normalize(keyword) in text for keyword in keywords):
            return bucket
    return "No clasificado"


def parse_money(value):
    cleaned = re.sub(r"[^\d,.]", "", str(value or ""))
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


def salary_from_text(text):
    cleaned = re.sub(r"\s+", " ", html.unescape(text or " "))
    patterns = [
        r"(RD\$|DOP|RD|US\$|USD)\s*([\d,.]+)\s*(?:-|a|hasta|–)\s*(?:RD\$|DOP|RD|US\$|USD)?\s*([\d,.]+)",
        r"([\d,.]+)\s*(?:-|a|hasta|–)\s*([\d,.]+)\s*(RD\$|DOP|RD|US\$|USD)",
        r"([\d,.]+)\s*\$\s*\(Mensual\)",
        r"(?:salario|sueldo|remuneracion|remuneración)\s*:?\s*(RD\$|DOP|RD|US\$|USD)?\s*([\d,.]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if not match:
            continue
        groups = [g for g in match.groups() if g]
        currency = next((g.upper().replace("$", "") for g in groups if re.search(r"RD\$|DOP|^RD$|US\$|USD", g, re.I)), "DOP")
        nums = [parse_money(g) for g in groups if parse_money(g)]
        if not nums:
            continue
        if len(nums) == 1:
            min_salary = max_salary = nums[0]
        else:
            min_salary, max_salary = min(nums[:2]), max(nums[:2])
        if currency == "US":
            currency = "USD"
        if currency == "RD":
            currency = "DOP"
        return currency, min_salary, max_salary
    return None, None, None


def strip_tags(fragment):
    fragment = re.sub(r"<script[\s\S]*?</script>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<style[\s\S]*?</style>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def title_from_fragment(fragment, fallback):
    candidates = [
        r"<h1[^>]*>([\s\S]{3,160}?)</h1>",
        r"<h2[^>]*>([\s\S]{3,160}?)</h2>",
        r"<h3[^>]*>([\s\S]{3,160}?)</h3>",
        r"title=\"([^\"]{3,160})\"",
        r"aria-label=\"([^\"]{3,160})\"",
    ]
    for pattern in candidates:
        match = re.search(pattern, fragment, re.I)
        if match:
            title = strip_tags(match.group(1))
            if len(title) >= 3:
                return title[:140]
    text = strip_tags(fragment)
    return (text[:100] or fallback).strip()


def extract_records(page_html, source_key, source_name, url, query):
    records = []
    text_records = extract_records_from_text(page_html, source_key, source_name, url, query)
    records.extend(text_records)

    chunks = re.split(r"(?i)(?:<article|<li|<div)", page_html)
    for chunk in chunks:
        if not re.search(r"RD\$|DOP|salario|sueldo|remuneraci[oó]n|US\$|USD", chunk, re.I):
            continue
        currency, salary_min, salary_max = salary_from_text(chunk)
        if not salary_min:
            continue
        title = title_from_fragment(chunk, query)
        records.append({
            "portal": source_name,
            "source_key": source_key,
            "source_url": url,
            "query": query,
            "title": title,
            "company": "",
            "location": "República Dominicana",
            "category": classify_role(title + " " + query),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_mid": round((salary_min + salary_max) / 2, 2),
            "currency": currency,
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "evidence": strip_tags(chunk)[:280],
        })
    return records


def extract_records_from_text(page_html, source_key, source_name, url, query):
    text = strip_tags(page_html)
    records = []
    salary_line_re = re.compile(r"((?:RD\$|DOP|US\$|USD)?\s*[\d,.]+\s*\$\s*\(Mensual\)|(?:RD\$|DOP|US\$|USD)\s*[\d,.]+)", re.I)
    noise = {"postular", "guardar en mis favoritos", "denunciar empleo", "ocultar oferta", "crear alerta"}
    bad_title_fragments = [
        "contraseña", "condiciones legales", "activar la alerta", "ya viste todas las ofertas",
        "has olvidado", "busqueda", "búsqueda", "cookies", "autorizacion", "autorización",
    ]

    for match in salary_line_re.finditer(text):
        line = match.group(1)
        currency, salary_min, salary_max = salary_from_text(line)
        if not salary_min:
            continue

        before = text[max(0, match.start() - 450):match.start()]
        segment = re.split(r"Oferta oculta Mostrar oferta|Mostrar oferta|Postular Guardar|Crear alerta", before)[-1]
        previous = [candidate.strip() for candidate in re.split(r"\s{2,}| Postulado Vista | Hace \\d+ | Ayer | Remoto | Presencial y remoto ", segment) if candidate.strip()]
        previous = [candidate for candidate in previous if normalize(candidate) not in noise and len(candidate) > 2]
        title = previous[-3] if len(previous) >= 3 else previous[0] if previous else query
        company = previous[-2] if len(previous) >= 2 else ""
        location = previous[-1] if previous else "República Dominicana"
        if any(fragment in normalize(title) for fragment in bad_title_fragments):
            continue

        records.append({
            "portal": source_name,
            "source_key": source_key,
            "source_url": url,
            "query": query,
            "title": title[:140],
            "company": company[:120],
            "location": location[:140],
            "category": classify_role(title + " " + query),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_mid": round((salary_min + salary_max) / 2, 2),
            "currency": currency,
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "evidence": line[:280],
        })
    return records


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 salary-research-bot/1.0",
            "Accept-Language": "es-DO,es;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def collect_from_source(source_key, terms, limit):
    source = SOURCES[source_key]
    records = []
    source_terms = terms[:limit] if "{query}" in source["url"] else ["categoria"]
    for idx, term in enumerate(source_terms, start=1):
        query = urllib.parse.quote(term)
        url = source["url"].format(query=query)
        print(f"  [{source_key} {idx}/{min(limit, len(terms))}] {term}")
        try:
            page = fetch(url)
            found = extract_records(page, source_key, source["name"], url, term)
            records.extend(found)
            print(f"      salarios visibles: {len(found)}")
        except Exception as exc:
            print(f"      error: {exc}")
        time.sleep(1.5)
    return records


def collect_from_html_dir(path):
    records = []
    for filename in sorted(os.listdir(path)):
        if not filename.lower().endswith((".html", ".htm", ".txt")):
            continue
        full_path = os.path.join(path, filename)
        with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
            page = fh.read()
        source_key = os.path.splitext(filename)[0].split("_")[0]
        source = SOURCES.get(source_key, {"name": source_key})
        found = extract_records(page, source_key, source["name"], full_path, filename)
        records.extend(found)
        print(f"  {filename}: {len(found)} salarios visibles")
    return records


def dedupe(records):
    output = []
    seen = set()
    for record in records:
        key = (
            normalize(record["portal"]),
            normalize(record["title"])[:80],
            int(record["salary_min"]),
            int(record["salary_max"]),
        )
        if key in seen:
            continue
        seen.add(key)
        output.append(record)
    return output


def write_outputs(records):
    records = dedupe(records)
    fields = [
        "portal", "source_key", "source_url", "query", "title", "company",
        "location", "category", "salary_min", "salary_max", "salary_mid",
        "currency", "captured_at", "evidence",
    ]
    with open(RAW_CSV, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    with open(RAW_JSON, "w", encoding="utf-8") as fh:
        json.dump({"capturedAt": datetime.now().isoformat(timespec="seconds"), "records": records}, fh, ensure_ascii=False, indent=2)
    print(f"\n[✓] Registros con salario visible: {len(records)}")
    print(f"    CSV:  {RAW_CSV}")
    print(f"    JSON: {RAW_JSON}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=sorted(SOURCES.keys()), help="Portal a consultar.")
    parser.add_argument("--all", action="store_true", help="Consulta todos los portales configurados.")
    parser.add_argument("--url", action="append", help="URL directa de una pagina de vacantes o salarios.")
    parser.add_argument("--computrabajo-steam", action="store_true", help="Consulta Computrabajo con terminos STEAM y categorias de informática/ingeniería.")
    parser.add_argument("--limit", type=int, default=len(SEARCH_TERMS), help="Cantidad de terminos por portal.")
    parser.add_argument("--term", action="append", help="Termino de busqueda adicional o reemplazo si se usa solo.")
    parser.add_argument("--html-dir", help="Directorio con HTML guardado manualmente de portales.")
    args = parser.parse_args()

    terms = args.term if args.term else SEARCH_TERMS
    records = []

    if args.html_dir:
        records.extend(collect_from_html_dir(args.html_dir))
    elif args.url:
        for url in args.url:
            print(f"  [url] {url}")
            page = fetch(url)
            records.extend(extract_records(page, "url", "URL directa", url, url))
    elif args.computrabajo_steam:
        records.extend(collect_from_source("computrabajo", terms, args.limit))
        records.extend(collect_from_source("computrabajo_it", terms, args.limit))
        records.extend(collect_from_source("computrabajo_engineering", terms, args.limit))
    elif args.all:
        for source_key in SOURCES:
            records.extend(collect_from_source(source_key, terms, args.limit))
    elif args.source:
        records.extend(collect_from_source(args.source, terms, args.limit))
    else:
        parser.print_help()
        return

    write_outputs(records)


if __name__ == "__main__":
    main()
