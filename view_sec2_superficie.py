with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Contraste Dimensional' in l:
        snip = ''.join(lines[i-15:i+60])
        print(snip.encode('ascii', 'replace').decode('ascii'))
        break
