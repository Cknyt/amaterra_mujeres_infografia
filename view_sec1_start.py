with open('new/reporte_diputacion_agro_3.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'bloque-subsectores' in l or 'Comparativa Directa de Especializaci' in l:
        print(''.join(lines[i-10:i+80]).encode('ascii', 'replace').decode('ascii'))
        break
