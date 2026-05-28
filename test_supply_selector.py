# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import urllib.parse
from datetime import datetime

# Configure stdout for UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_PATH = os.path.join(WORKSPACE, "search_screenshot.png")

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
    print("======================================================================")
    # Start Chrome
    driver, WebDriverWait, By = setup_driver()
    
    print("[🔐] Abriendo LinkedIn Login para diagnóstico...")
    driver.get("https://www.linkedin.com/login?lang=es")
    time.sleep(2)
    print("\nInicia sesión en Chrome. El script de diagnóstico continuará cuando inicies sesión.\n")
    
    # Wait for login
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
        print("[✓] Sesión iniciada.")
    except Exception:
        print("[x] Tiempo agotado esperando login.")
        driver.quit()
        sys.exit(1)

    url = linkedin_people_url(KEYWORDS)
    print(f"\n[🔍] Navigando a la búsqueda de prueba: {url}")
    driver.get(url)
    time.sleep(8) # Wait for page and search results to load fully
    
    # Save screenshot
    driver.save_screenshot(SCREENSHOT_PATH)
    print(f"[📸] Captura de pantalla guardada en: {SCREENSHOT_PATH}")
    
    # Inspect elements
    print("\n--- DIAGNÓSTICO DE SELECTORES ---")
    
    # Dump title and current URL
    print(f"URL actual: {driver.current_url}")
    print(f"Título de la página: {driver.title}")
    
    # List elements that might contain the result count
    selectors_to_check = [
        "h2",
        "h1",
        "div",
        "span",
        "p",
        ".search-results-container h2",
        ".pb2.t-black--light.t-14",
        ".search-results__total",
        "main",
    ]
    
    found_texts = []
    
    # Let's check general tags for result-like texts
    for tag in ["h1", "h2", "h3", "span", "div", "p"]:
        try:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for el in elements:
                try:
                    text = el.text.strip()
                    if text and any(word in text.lower() for word in ["resultado", "result", "persona", "people", "cerca de", "about"]):
                        found_texts.append(f"<{tag}>: {text[:150]}")
                except:
                    continue
        except Exception as e:
            print(f"Error checking tag {tag}: {e}")
            
    # Print distinct matching texts
    distinct_found = sorted(list(set(found_texts)))
    print(f"\nSe encontraron {len(distinct_found)} textos candidatos conteniendo palabras clave:")
    for text in distinct_found[:30]:
        print(f"  * {text}")
        
    # Write page source snippets to a text file for inspection
    html_source = driver.page_source
    source_snippet_path = os.path.join(WORKSPACE, "search_page_source_snippet.html")
    with open(source_snippet_path, "w", encoding="utf-8") as f:
        # Write first 50000 characters of page source
        f.write(html_source[:100000])
    print(f"\n[✓] Primeros 100k caracteres del código fuente guardados en: {source_snippet_path}")
    
    driver.quit()

if __name__ == "__main__":
    main()
