# compare_all_tables.py
import openpyxl
import re
import json

wb = openpyxl.load_workbook('20260925_DatosExplotaciones.xlsx', data_only=True)
ws_no = wb['No_ATP']
ws_atp = wb['ATP']

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract DATA_EXCEL from html
m = re.search(r'const DATA_EXCEL\s*=\s*(\{.+?\});\s*(?:const|function|let|var)', html, re.DOTALL)
if not m:
    print("Could not extract DATA_EXCEL")
    exit(1)

# Clean and parse DATA_EXCEL as JSON (or evaluate)
js_code = m.group(1)
# Write to temp file and parse with node
with open('temp_data.js', 'w', encoding='utf-8') as f:
    f.write('console.log(JSON.stringify(' + js_code + '));')

import subprocess
res = subprocess.run(['node', 'temp_data.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
data_html = json.loads(res.stdout)

print("="*70)
print("1. MARCO GENERAL")
print("="*70)
print("EXCEL Hoja No_ATP rows 3-12:")
print("Censo total: Hombres=8462, Mujeres=3664, Total=12126 (en html: h=8458, m=3662, tot=12120)")
print("Autoconsumo: Hombres=6335, Mujeres=2470, Total=8805")
print("Fines mercado: Hombres=2129, Mujeres=1194, Total=3323")
print("No ATP mercado (row 16): Hombres=1789, Mujeres=1004, Total=2793")
print("ATP total (row 6): Total=529 (H=339, M=190)")

print("\n" + "="*70)
print("2. EDAD - ATP")
print("="*70)
print("EXCEL ATP rows 29-33 (cols 16-20):")
print("Edad media:", ws_atp.cell(30, 4).value)
for r in range(30, 33):
    tramo = ws_atp.cell(r, 16).value
    h = ws_atp.cell(r, 17).value
    m = ws_atp.cell(r, 18).value
    hp = ws_atp.cell(r, 19).value
    mp = ws_atp.cell(r, 20).value
    print(f"Excel ATP Edad {tramo}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.ATP.edad:", data_html['ATP']['edad'])

print("\n" + "="*70)
print("3. EDAD - NO ATP")
print("="*70)
print("EXCEL No_ATP rows 20-22:")
print("Edad media: H=", ws_no.cell(26, 4).value, "M=", ws_no.cell(26, 5).value)
for r in range(20, 23):
    tramo = ws_no.cell(r, 3).value
    h = ws_no.cell(r, 4).value
    m = ws_no.cell(r, 5).value
    hp = ws_no.cell(r, 6).value
    mp = ws_no.cell(r, 7).value
    print(f"Excel No_ATP Edad {tramo}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.No_ATP.edad:", data_html['No_ATP']['edad'])

print("\n" + "="*70)
print("4. SUPERFICIE - ATP")
print("="*70)
print("EXCEL ATP rows 33-36:")
for r in range(33, 37):
    estrato = ws_atp.cell(r, 4).value
    h = ws_atp.cell(r, 5).value
    m = ws_atp.cell(r, 7).value
    mp = ws_atp.cell(r, 9).value
    hp = ws_atp.cell(r, 10).value
    print(f"Excel ATP Superficie {estrato}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.ATP.superficie:", data_html['ATP']['superficie'])

print("\n" + "="*70)
print("5. SUPERFICIE - NO ATP")
print("="*70)
print("EXCEL No_ATP rows 57-60:")
for r in range(57, 61):
    estrato = ws_no.cell(r, 4).value
    h = ws_no.cell(r, 5).value
    m = ws_no.cell(r, 7).value
    hp = ws_no.cell(r, 6).value
    mp = ws_no.cell(r, 8).value
    print(f"Excel No_ATP Superficie {estrato}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.No_ATP.superficie:", data_html['No_ATP']['superficie'])

print("\n" + "="*70)
print("6. COMARCAS - ATP")
print("="*70)
print("EXCEL ATP rows 45-50:")
for r in range(45, 51):
    comarca = ws_atp.cell(r, 4).value
    h = ws_atp.cell(r, 5).value
    m = ws_atp.cell(r, 7).value
    mp = ws_atp.cell(r, 9).value # % de las 190 mujeres
    hp = ws_atp.cell(r, 10).value # % de los 339 hombres
    print(f"Excel ATP Comarca {comarca.strip()}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.ATP.comarca:", data_html['ATP']['comarca'])

print("\n" + "="*70)
print("7. COMARCAS - NO ATP")
print("="*70)
print("EXCEL No_ATP rows 71-76:")
for r in range(71, 77):
    comarca = ws_no.cell(r, 4).value
    h = ws_no.cell(r, 5).value
    m = ws_no.cell(r, 7).value
    hp = ws_no.cell(r, 6).value
    mp = ws_no.cell(r, 8).value
    print(f"Excel No_ATP Comarca {comarca.strip()}: H={h} ({hp:.2f}%), M={m} ({mp:.2f}%)")
print("HTML DATA_EXCEL.No_ATP.comarca:", data_html['No_ATP']['comarca'])

print("\n" + "="*70)
print("8. ECOLOGICO - ATP")
print("="*70)
print("EXCEL ATP rows 40-41:")
print("Row 40 Certificado ecológico:", "H=", ws_atp.cell(40, 5).value, "H%=", ws_atp.cell(40, 6).value, "M=", ws_atp.cell(40, 7).value, "M%=", ws_atp.cell(40, 8).value)
print("Total ecos (row 39, col 12):", ws_atp.cell(39, 12).value)
print("HTML DATA_EXCEL.ATP.ecologico:", data_html['ATP']['ecologico'])

print("\n" + "="*70)
print("9. SUBSECTORES - ATP")
print("="*70)
print("EXCEL ATP rows 13-26:")
for r in range(13, 27):
    nom = ws_atp.cell(r, 4).value
    h = ws_atp.cell(r, 5).value
    m = ws_atp.cell(r, 6).value
    mp = ws_atp.cell(r, 9).value
    print(f"Excel ATP Subsector {nom}: H={h}, M={m}, M%={mp:.2f}%")

print("\n" + "="*70)
print("10. SUBSECTORES - NO ATP")
print("="*70)
print("EXCEL No_ATP rows 30-47:")
for r in range(30, 48):
    nom = ws_no.cell(r, 4).value
    h = ws_no.cell(r, 5).value
    m = ws_no.cell(r, 6).value
    hp = ws_no.cell(r, 7).value
    mp = ws_no.cell(r, 8).value
    print(f"Excel No_ATP Subsector {nom}: H={h}, M={m}, M%={mp:.2f}%")
