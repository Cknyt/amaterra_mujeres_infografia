with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'txt-sec1-noatp-text' in l:
        print(''.join(lines[i:i+60]))
        break
