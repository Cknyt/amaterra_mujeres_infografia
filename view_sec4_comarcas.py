with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="bloque-comarcas"' in l:
        snip = ''.join(lines[i:i+80])
        print(snip.encode('ascii', 'replace').decode('ascii'))
        break
