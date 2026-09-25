import re

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'function setLang\(lang\)\s*\{(.*?)\n\s*function\s+', html, re.DOTALL)
if m:
    fn_body = m.group(1)
    calls = re.findall(r'setEl(?:Text|Html)\(\s*[\'"]([^\'"]+)[\'"]', fn_body)
    print(f"Total setEl calls: {len(calls)}")
    missing = []
    for el_id in calls:
        if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html:
            print(f"MISSING ID: {el_id}")
            missing.append(el_id)
    if not missing:
        print("All setEl IDs exist in HTML!")

# Also check for document.getElementById in setLang or elsewhere
all_get_ids = re.findall(r'document\.getElementById\(\s*[\'"]([^\'"]+)[\'"]', fn_body)
for el_id in all_get_ids:
    if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html:
        print(f"MISSING getElementById: {el_id}")

# Also check badge loop in setLang
badge_loop = re.search(r'for\s*\(let i = 1;\s*i\s*<=\s*(\d+);\s*i\+\+\)\s*\{\s*setElText\([\'"]badge-atp-pill-[\'"]\s*\+\s*i', fn_body)
if badge_loop:
    print(f"Badge loop max: {badge_loop.group(1)}")
    for i in range(1, int(badge_loop.group(1)) + 1):
        if f'id="badge-atp-pill-{i}"' not in html:
            print(f"MISSING badge-atp-pill-{i}")
        if f'id="badge-noatp-pill-{i}"' not in html:
            print(f"MISSING badge-noatp-pill-{i}")
