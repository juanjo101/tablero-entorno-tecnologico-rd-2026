import os
import requests
import time
from urllib.parse import urlparse
import re

# Diccionario de búsquedas: Universidad -> Lista de carreras
universidades = {
    "intec.edu.do": ["Ingeniería Ciberseguridad", "Ingeniería en Sistemas", "Licenciatura en Ciencias de Datos"],
    "itla.edu.do": ["Tecnólogo Ciberseguridad", "Tecnólogo Desarrollo de Software"],
    "uasd.edu.do": ["Ingeniería de Sistemas", "Ciencia de Datos"],
    "pucmm.edu.do": ["Ingeniería Computación e Inteligencia Artificial", "Ciberseguridad"],
    "udoym.edu.do": ["Ingeniería Sistemas y Computación"],
    "uapa.edu.do": ["Ingeniería en Software"],
    "unicaribe.edu.do": ["Ingeniería Ciberseguridad"],
    "unicda.edu.do": ["Ingeniería Software", "Ingeniería Ciencia de Datos"]
}

# Crear directorio
os.makedirs("planes_estudio", exist_ok=True)

# Fake User-Agent para peticiones
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def buscar_y_descargar():
    print("Iniciando búsqueda automatizada de pénsumes en PDF...\n")
    
    # Se genera un archivo CSV con el reporte de enlaces descubiertos
    with open("enlaces_exactos.csv", "w", encoding="utf-8") as f_csv:
        f_csv.write("Universidad,Carrera,Enlace_Descubierto,Estado\n")
        
        for dominio, carreras in universidades.items():
            for carrera in carreras:
                query = f"filetype:pdf pensum {carrera} site:{dominio}"
                print(f"[*] Buscando: {query}")
                
                # Búsqueda en texto plano para evitar captchas pesados de Google
                search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
                try:
                    resp = requests.get(search_url, headers=HEADERS, timeout=15)
                    resp.raise_for_status()
                    
                    # Extraer el primer enlace que termine en PDF
                    enlaces_pdf = re.findall(r'href="([^"]+\.pdf)"', resp.text, re.IGNORECASE)
                    
                    # Si DuckDuckGo ofusca la URL, intentamos extraer la URL de destino
                    raw_urls = re.findall(r'href="[^"]+uddg=([^"&]+)', resp.text)
                    if raw_urls:
                        # Decodificar URL
                        enlaces_pdf = [requests.utils.unquote(u) for u in raw_urls if u.lower().endswith('.pdf')]
                        
                    if enlaces_pdf:
                        pdf_url = enlaces_pdf[0]
                        if pdf_url.startswith('//'):
                            pdf_url = 'https:' + pdf_url
                            
                        print(f" -> Encontrado: {pdf_url}")
                        
                        # Intentar descargar el PDF
                        try:
                            pdf_resp = requests.get(pdf_url, headers=HEADERS, timeout=20)
                            pdf_resp.raise_for_status()
                            
                            # Nombre seguro para el archivo
                            safe_name = f"{dominio.split('.')[0]}_{carrera.replace(' ', '_')}.pdf"
                            filepath = os.path.join("planes_estudio", safe_name)
                            
                            with open(filepath, "wb") as pdf_file:
                                pdf_file.write(pdf_resp.content)
                                
                            print(f" -> Descargado correctamente: {filepath}")
                            f_csv.write(f"{dominio},{carrera},{pdf_url},Descargado\n")
                            
                        except Exception as e_descarga:
                            print(f" -> Error al descargar el PDF: {e_descarga}")
                            f_csv.write(f"{dominio},{carrera},{pdf_url},Error Descarga\n")
                    else:
                        print(" -> No se encontraron resultados directos en formato PDF.")
                        f_csv.write(f"{dominio},{carrera},N/A,No Encontrado\n")
                        
                except Exception as e_busqueda:
                    print(f" -> Error en la petición de búsqueda: {e_busqueda}")
                    f_csv.write(f"{dominio},{carrera},N/A,Error Búsqueda\n")
                    
                # Pausa ética para evitar bloqueos por rate-limiting
                time.sleep(3) 

    print("\n[+] Proceso finalizado. Revisa la carpeta 'planes_estudio/' y el archivo 'enlaces_exactos.csv'.")

if __name__ == "__main__":
    buscar_y_descargar()
