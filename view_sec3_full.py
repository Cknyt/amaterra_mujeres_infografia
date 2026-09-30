with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(''.join(lines[1775:1840]).encode('ascii', 'replace').decode('ascii'))
