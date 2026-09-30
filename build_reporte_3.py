# -*- coding: utf-8 -*-
"""
Build reporte_diputacion_agro_3.html in the new/ folder from reporte_diputacion_agro_2.html,
updating DATA_EXCEL with the new No ATP data (UTAs >= 0.5: 232 women, 459 men, 691 total)
and updating all relevant UI texts, badges, micro-KPIs, and I18N labels.
"""
import re
import json

def build_reporte_3():
    with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Load new No_ATP data
    with open('new_noatp_data.json', 'r', encoding='utf-8') as f:
        new_no_atp = json.load(f)

    # 1. Update DATA_EXCEL inside HTML
    match = re.search(r'const DATA_EXCEL = (\{.+?\});\s*(?:const|function|let|var)', html, re.DOTALL)
    if not match:
        raise ValueError("Could not find DATA_EXCEL in reporte_diputacion_agro_2.html")

    # Extract ATP from current DATA_EXCEL so we preserve it completely
    # We can evaluate or extract it cleanly
    import subprocess
    js_extract = f"""
    const fs = require('fs');
    const html = fs.readFileSync('reporte_diputacion_agro_2.html', 'utf8');
    const match = html.match(/const DATA_EXCEL = (\{{.+?\}});\\s*(?:const|function|let|var)/s);
    const data = eval('(' + match[1] + ')');
    const newNoAtp = JSON.parse(fs.readFileSync('new_noatp_data.json', 'utf8'));
    data.No_ATP = newNoAtp;
    fs.writeFileSync('new_data_excel.json', JSON.stringify(data, null, 2), 'utf8');
    """
    with open('temp_merge.js', 'w', encoding='utf-8') as tf:
        tf.write(js_extract)
    subprocess.run(['node', 'temp_merge.js'], check=True)

    with open('new_data_excel.json', 'r', encoding='utf-8') as f:
        merged_data_excel = f.read()

    # Replace DATA_EXCEL block in HTML
    old_data_excel_block = match.group(0)
    # The ending token was captured as well (const/function/etc.), keep it
    end_token = re.search(r';\s*(const|function|let|var)$', old_data_excel_block).group(1)
    new_data_excel_block = f"const DATA_EXCEL = {merged_data_excel};\n\n  {end_token}"
    html = html[:match.start()] + new_data_excel_block + html[match.end():]

    # 2. Update UI Texts & Labels for No ATP (232 mujeres >=0.5 UTAs en vez de 1.004)
    # Hero Stat 4
    html = re.sub(
        r'<div class="hero-stat-val" id="txt-kpi4-val"[^>]*>1\.004 Mujeres</div>\s*<div class="hero-stat-desc" id="txt-kpi4-desc">35,9% de los 2\.793 No ATPs comerciales</div>',
        '<div class="hero-stat-val" id="txt-kpi4-val" style="color: #FCD34D;">232 Mujeres</div>\n          <div class="hero-stat-desc" id="txt-kpi4-desc">33,6% de los 691 No ATPs comerciales (≥0,5 UTAs)</div>',
        html
    )

    # View Mode Button
    html = re.sub(
        r'<span id="txt-view-noatp">Solo NO ATP \(1\.004 mujeres\)</span>',
        '<span id="txt-view-noatp">Solo NO ATP (232 mujeres ≥0,5 UTAs)</span>',
        html
    )

    # Section badges & descriptions
    html = html.replace('NO ATP: 1.004 Mujeres', 'NO ATP: 232 Mujeres (≥0,5 UTAs)')
    html = html.replace('(1.004 mujeres)', '(232 mujeres ≥0,5 UTAs)')
    html = html.replace('1.004 titulares', '232 titulares')
    html = html.replace('de 1004', 'de 232')
    html = html.replace('1004tik', '232tik')
    html = html.replace('1004 ${mLabel}', '232 ${mLabel}')

    # I18N dictionary updates
    html = html.replace('"1.004 Mujeres"', '"232 Mujeres"')
    html = html.replace('"35,9% de los 2.793 No ATPs comerciales"', '"33,6% de los 691 No ATPs comerciales (≥0,5 UTAs)"')
    html = html.replace('"Solo NO ATP (1.004 mujeres)"', '"Solo NO ATP (232 mujeres ≥0,5 UTAs)"')
    html = html.replace('"1.004 Emakume"', '"232 Emakume"')
    html = html.replace('"2.793 Ez-ATP komertzialen %35,9"', '"691 Ez-ATP komertzialen %33,6 (≥0,5 UTA)"')
    html = html.replace('"Ez-ATP soilik (1.004 emakume)"', '"Ez-ATP soilik (232 emakume ≥0,5 UTA)"')

    # Micro-KPIs Section 5 (Edad)
    html = re.sub(
        r'<span class="micro-kpi-val atp-text">53 vs 66</span>\s*<span class="micro-kpi-lbl">Brecha de Edad Media · \+13 años en NO ATP</span>',
        '<span class="micro-kpi-val atp-text">53 vs 64</span>\n          <span class="micro-kpi-lbl">Brecha de Edad Media · +11 años en NO ATP</span>',
        html
    )
    html = re.sub(
        r'<span class="micro-kpi-val atp-text">72,63%</span>\s*<span class="micro-kpi-lbl">Madurez Productiva ATP · 41-65 años \(138 titulares\)</span>',
        '<span class="micro-kpi-val atp-text">72,6% vs 41,4%</span>\n          <span class="micro-kpi-lbl">Madurez Productiva · 41-65 años (138 ATP vs 96 NO ATP)</span>',
        html
    )
    html = re.sub(
        r'<span class="micro-kpi-val noatp-text">74,20%</span>\s*<span class="micro-kpi-lbl">Edad de Jubilación NO ATP · >65 años \(745 titulares\)</span>',
        '<span class="micro-kpi-val noatp-text">51,3%</span>\n          <span class="micro-kpi-lbl">Edad de Jubilación NO ATP · >65 años (119 titulares)</span>',
        html
    )
    html = re.sub(
        r'<span class="micro-kpi-val atp-text">17,4% vs 5,8%</span>\s*<span class="micro-kpi-lbl">Tasa de Juventud · 18-40 años \(Triple en ATP\)</span>',
        '<span class="micro-kpi-val atp-text">17,4% vs 7,3%</span>\n          <span class="micro-kpi-lbl">Tasa de Juventud · 18-40 años (33 ATP vs 17 NO ATP)</span>',
        html
    )

    # Alert Box Section 5 (Edad)
    html = re.sub(
        r'<strong style="color: #DC2626;">Alerta Demográfica:</strong> <strong>745 mujeres \(74,2%\) superan los 65 años</strong> \(frente al 60,5% de los hombres\)\. Casi tres de cada cuatro explotaciones comerciales no profesionales afrontan riesgo inminente de cese en esta década por jubilación sin relevo tutelado\.',
        '<strong style="color: #DC2626;">Alerta Demográfica:</strong> <strong>119 mujeres (51,3%) superan los 65 años</strong> (frente al 27,0% de los hombres). Más de la mitad de las explotaciones comerciales no profesionales (≥0,5 UTAs) afrontan riesgo de cese en esta década por jubilación sin relevo tutelado.',
        html
    )

    # Insight pill text Section 5
    html = re.sub(
        r'Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> \(53 años en ATP frente a 66 años en No ATP\)\. En el colectivo No ATP, <strong>casi tres de cada cuatro mujeres \(74,2% - 745 titulares\) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,8% \(58 mujeres\)\. Sin un plan de relevo tutelado, más de 700 explotaciones corren riesgo de cese en la presente década\.',
        'Existe una brecha generacional de <strong>11 años en la edad media</strong> (53 años en ATP frente a 64 años en No ATP). En el colectivo No ATP (≥0,5 UTAs), <strong>más de la mitad de las mujeres (51,3% - 119 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años suponen el 7,3% (17 mujeres). Sin un plan de relevo tutelado, más de 100 explotaciones activas corren riesgo de cese en la presente década.',
        html
    )

    # Micro-KPIs Section 1 (Subsectores)
    html = re.sub(
        r'<div class="insight-metric-val">44,6%</div>\s*<div class="insight-metric-label">Bovino Carne \(448 titulares\)</div>',
        '<div class="insight-metric-val">66,8%</div>\n                    <div class="insight-metric-label">Bovino Carne (155 titulares)</div>',
        html
    )
    html = re.sub(
        r'<div class="insight-metric-val">12,2%</div>\s*<div class="insight-metric-label">Ovino \(122 titulares\)</div>',
        '<div class="insight-metric-val">8,2%</div>\n                    <div class="insight-metric-label">Hortalizas Invernadero (19 titulares)</div>',
        html
    )
    html = re.sub(
        r'<div class="insight-metric-val">10,4%</div>\s*<div class="insight-metric-label">No Clasificadas \(104 titulares\)</div>',
        '<div class="insight-metric-val">7,8%</div>\n                    <div class="insight-metric-label">Ovino (18 titulares)</div>',
        html
    )

    # Title tag update
    html = html.replace('<title>Mujeres en el Sector Agroganadero de Bizkaia | Análisis Oficial Diputación</title>',
                        '<title>Mujeres en el Sector Agroganadero de Bizkaia | Reporte Oficial v3 (Filtro UTAs ≥ 0,5)</title>')

    # Write to target file
    output_path = 'new/reporte_diputacion_agro_3.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Successfully generated {output_path} with length {len(html)} bytes!")

if __name__ == '__main__':
    build_reporte_3()
