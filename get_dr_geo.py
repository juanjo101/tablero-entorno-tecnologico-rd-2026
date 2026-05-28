# -*- coding: utf-8 -*-
import sys
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=es-419")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    print("[+] Iniciando Chrome para capturar la ubicación correcta de República Dominicana...")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except Exception as e:
        print(f"[x] Error iniciando Chrome: {e}")
        sys.exit(1)

    print("\n" + "="*80)
    print(" 1. Inicia sesión en la ventana de Chrome de LinkedIn que se abrió.")
    print(" 2. El script te llevará automáticamente a una página de búsqueda.")
    print(" 3. Haz clic en el botón verde de ubicación (el que dice Hornchurch / Inglaterra).")
    print(" 4. Quita Inglaterra presionando la 'X', escribe 'República Dominicana' y elígela.")
    print(" 5. Presiona 'Ver resultados'.")
    print(" 6. ¡El script detectará el nuevo código de forma automática y se cerrará solo!")
    print("="*80 + "\n")

    # Ir a login
    driver.get("https://www.linkedin.com/login?lang=es")

    # Esperar inicio de sesión
    logged_in = False
    while not logged_in:
        try:
            url = driver.current_url
            if any(k in url for k in ["linkedin.com/feed", "linkedin.com/search", "linkedin.com/mynetwork", "linkedin.com/in/", "linkedin.com/home"]):
                logged_in = True
                print("[✓] Inicio de sesión detectado.")
                break
        except Exception:
            pass
        time.sleep(1)

    # Redirigir a una búsqueda inicial con la ubicación incorrecta para que la cambien
    time.sleep(2)
    driver.get('https://www.linkedin.com/search/results/people/?keywords=ciberseguridad&geoUrn=%5B"101623149"%5D')
    print("[+] Cargada búsqueda inicial. Cambia el filtro de ubicación en tu navegador...")

    # Monitorear la URL hasta que cambie
    try:
        while True:
            url = driver.current_url
            # Buscar geoUrn en la URL que no sea el erróneo 101623149
            if "geoUrn=" in url and "%22101623149%22" not in url and '"101623149"' not in url:
                print(f"\n[🎉] ¡Cambio de ubicación detectado en el navegador!")
                
                # Intentar parsear el ID
                match = (re.search(r'geoUrn=%5B%22(\d+)%22%5D', url) or 
                         re.search(r'geoUrn=\["(\d+)"\]', url) or 
                         re.search(r'geoUrn=%5B"(\d+)"%5D', url))
                if match:
                    geo_id = match.group(1)
                    print("\n" + "="*60)
                    print(f" 🏆 CÓDIGO DE REPÚBLICA DOMINICANA DETECTADO: {geo_id}")
                    print("="*60 + "\n")
                    
                    # Guardar en archivo temporal
                    with open("dr_geo_id.txt", "w") as f:
                        f.write(geo_id)
                    break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[x] Cancelado por el usuario.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
