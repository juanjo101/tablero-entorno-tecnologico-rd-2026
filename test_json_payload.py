# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import re
import urllib.parse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
GEO_URN_RD = "101623149"
KEYWORDS = "prompt engineering OR IA generativa OR generative AI OR ChatGPT"

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
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=es-419")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver, WebDriverWait, By

def main():
    driver, WebDriverWait, By = setup_driver()
    driver.get("https://www.linkedin.com/login?lang=es")
    time.sleep(2)
    print("\nInicia sesión para inspeccionar el payload JSON...\n")
    
    try:
        WebDriverWait(driver, 180).until(
            lambda d: (
                "linkedin.com/feed" in d.current_url
                or "linkedin.com/search" in d.current_url
            ) and "login" not in d.current_url
        )
        time.sleep(3)
    except Exception:
        driver.quit()
        sys.exit(1)

    url = linkedin_people_url(KEYWORDS)
    print(f"\n[🔍] Navigando a la búsqueda: {url}")
    driver.get(url)
    time.sleep(8)
    
    # Save the full page source
    html_source = driver.page_source
    full_source_path = os.path.join(WORKSPACE, "full_search_page.html")
    with open(full_source_path, "w", encoding="utf-8") as f:
        f.write(html_source)
    print(f"[✓] Código fuente completo guardado en: {full_source_path}")
    
    # Let's extract all <code> tags
    code_tags = driver.find_elements(By.TAG_NAME, "code")
    print(f"\nSe encontraron {len(code_tags)} etiquetas <code>.")
    
    potential_totals = []
    
    for idx, tag in enumerate(code_tags):
        try:
            # We want display none ones
            id_attr = tag.get_attribute("id")
            style_attr = tag.get_attribute("style")
            inner_html = tag.get_attribute("innerHTML").strip()
            
            # Check if it starts with comment comment
            if inner_html.startswith("<!--") and inner_html.endswith("-->"):
                json_str = inner_html[4:-3].strip()
            else:
                json_str = inner_html
                
            if not json_str:
                continue
                
            try:
                data = json.loads(json_str)
                # Let's search inside data recursively for paging or total
                def recursive_search(obj, path=""):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            current_path = f"{path}.{k}" if path else k
                            if k.lower() in ["total", "totalresults", "numresults", "paging", "count"]:
                                potential_totals.append((current_path, v))
                            recursive_search(v, current_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            recursive_search(item, f"{path}[{i}]")
                
                recursive_search(data)
            except Exception:
                # Not valid JSON, skip
                continue
        except Exception as e:
            continue
            
    print(f"\nResultados de la búsqueda recursiva de campos relacionados a totales/conteo ({len(potential_totals)} encontrados):")
    for path, val in potential_totals:
        print(f"  * {path} = {val}")
        
    driver.quit()

if __name__ == "__main__":
    main()
