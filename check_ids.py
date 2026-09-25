with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# find all ids in html
dom_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

# find all getElementById in script
js_calls = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', html)

missing = {}
for i in js_calls:
    if i not in dom_ids:
        missing[i] = missing.get(i, 0) + 1

print("Missing IDs found in getElementById:", missing)
