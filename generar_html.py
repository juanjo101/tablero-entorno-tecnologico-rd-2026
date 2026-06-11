import urllib.request
import json
import os

with open('articulo_cientifico_brecha_talento.md', 'r', encoding='utf-8') as f:
    text = f.read()

try:
    import markdown
    html = markdown.markdown(text, extensions=['tables'])
    print('Usando markdown local.')
except ImportError:
    print('Usando API de GitHub para renderizar Markdown.')
    url = 'https://api.github.com/markdown'
    data = json.dumps({'text': text, 'mode': 'gfm'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')

html_output = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Artículo Científico - Brecha de Talento</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #333; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; }}
th, td {{ border: 1px solid #c0c0c0; padding: 10px; text-align: left; }}
th {{ background-color: #f0f4f8; color: #2c3e50; }}
img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 20px 0; }}
h1, h2, h3, h4 {{ color: #1a365d; margin-top: 30px; }}
h1 {{ border-bottom: 2px solid #1a365d; padding-bottom: 10px; }}
hr {{ border: 0; height: 1px; background: #e2e8f0; margin: 30px 0; }}
blockquote {{ border-left: 4px solid #1a365d; margin: 0; padding-left: 15px; color: #555; }}
</style>
</head>
<body>
{html}
</body>
</html>"""

with open('articulo_final.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("¡Archivo articulo_final.html generado exitosamente!")
