with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Sobrerrepresentaci' in l:
        snip = ''.join(lines[i-10:i+35])
        print(snip.encode('ascii', 'replace').decode('ascii'))
        break
