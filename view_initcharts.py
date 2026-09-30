with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function initCharts' in l:
        print(''.join(lines[i:i+80]).encode('ascii', 'replace').decode('ascii'))
        break
