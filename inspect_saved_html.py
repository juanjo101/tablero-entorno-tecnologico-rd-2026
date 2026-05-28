# -*- coding: utf-8 -*-
import os
import re
import json

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(WORKSPACE, "full_search_page.html")

def main():
    if not os.path.exists(HTML_PATH):
        print(f"No existe: {HTML_PATH}")
        return

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"Tamaño de full_search_page.html: {len(html)} caracteres")

    # 1. Search for any script tags with JSON
    script_json = re.findall(r'<script[^>]*type=["\']application/json["\'][^>]*>([\s\S]*?)</script>', html)
    print(f"Se encontraron {len(script_json)} etiquetas <script type='application/json'>")

    # 2. Search for any code tags (in case they were present but selenium didn't fetch them)
    code_tags = re.findall(r'<code[^>]*>([\s\S]*?)</code>', html)
    print(f"Se encontraron {len(code_tags)} etiquetas <code> en el HTML crudo.")

    # Let's inspect some code tag content if any
    for idx, c in enumerate(code_tags[:5]):
        print(f"  Code tag [{idx}]: len={len(c)}, snippet={c[:100]}...")

    # 3. Search for any mentions of "resultados" or "personas" with preceding numbers
    # We want to see if the count is present anywhere in the text or comments
    print("\n--- Búsqueda de patrones de conteo en el HTML crudo ---")
    patterns = [
        r'([\d.,]+)\s+(?:resultados|results|persona|personas|people)',
        r'(?:total|count|paging)[\s\S]{0,50}?([\d,.]+)',
    ]
    for pat in patterns:
        matches = re.findall(pat, html, re.IGNORECASE)
        if matches:
            # unique non-empty matches
            unique_matches = sorted(list(set([m.strip() for m in matches if m.strip()])))
            print(f"Patrón '{pat}' encontró {len(unique_matches)} coincidencias:")
            for m in unique_matches[:15]:
                # find context of the match
                start_indices = [i.start() for i in re.finditer(re.escape(m), html)]
                for idx_c, start_idx in enumerate(start_indices[:2]):
                    context = html[max(0, start_idx - 60):min(len(html), start_idx + 60)].replace('\n', ' ')
                    print(f"  * Context: ... {context} ...")

    # 4. Search for the Premium upsell box in the HTML to see its surrounding text
    print("\n--- Búsqueda de contexto de Premium ---")
    premium_matches = re.finditer(r'beneficiarte de búsquedas ilimitadas', html)
    for m in premium_matches:
        start = m.start()
        context = html[max(0, start-100):min(len(html), start+200)].replace('\n', ' ')
        print(f"  * Context Premium: ... {context} ...")

if __name__ == "__main__":
    main()
