with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# 1. Tables
matches = re.findall(r'<table[^>]*>.*?</table>', text, re.DOTALL)
print(f'Total tables found: {len(matches)}')
for i, t in enumerate(matches):
    ths = re.findall(r'<th[^>]*>(.*?)</th>', t)
    clean_ths = [re.sub(r'<[^>]+>', '', th).strip().encode('ascii', 'replace').decode('ascii') for th in ths]
    print(f'Table {i}: {clean_ths}')

# 2. Search for phrases mentioned by user:
phrases = [
    "Comparativa Directa",
    "Especializaci.n Productiva",
    "Vacuno Total",
    "Bases viables",
    "Sobrerrepresentaci.n Femenina",
    "Basti.n profesional",
    "Mayor polo comercial",
    "Urremendi (43%) vs Jata Ondo (26%)",
    "Contraste Dimensional",
    "Distribuci.n Comarcal Comparativa",
    "No clasificadas",
    "Ovinas"
]

print("\n--- Phrase matches ---")
for p in phrases:
    m = list(re.finditer(p, text, re.IGNORECASE))
    print(f'"{p}": {len(m)} matches')
    if m:
        for match in m[:2]:
            snippet = text[max(0, match.start()-60):min(len(text), match.end()+60)].replace('\n', ' ')
            clean_snip = snippet.encode('ascii', 'replace').decode('ascii')
            print(f'    ...{clean_snip}...')
