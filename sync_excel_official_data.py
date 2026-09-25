# sync_excel_official_data.py
import re

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero stats
content = re.sub(
    r'<div class="hero-stat-val">12\.120</div>\s*<div class="hero-stat-desc" id="txt-kpi1-desc">3\.662 Mujeres \(30,2%\) \| 8\.458 Hombres</div>',
    '<div class="hero-stat-val">12.126</div>\n          <div class="hero-stat-desc" id="txt-kpi1-desc">3.664 Mujeres (30,2%) | 8.462 Hombres</div>',
    content
)
content = re.sub(
    r'<div class="hero-stat-val">3\.322</div>\s*<div class="hero-stat-desc" id="txt-kpi2-desc">1\.194 Mujeres \(35,9%\) \| 2\.128 Hombres</div>',
    '<div class="hero-stat-val">3.323</div>\n          <div class="hero-stat-desc" id="txt-kpi2-desc">1.194 Mujeres (35,9%) | 2.129 Hombres</div>',
    content
)

# 2. Update Bloque 5 Micro-KPIs & Alert boxes
old_sec5_kpis = """      <!-- Micro-KPIs Resumen Edad y Relevo -->
      <div class="micro-kpi-grid">
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">53 vs 66</span>
          <span class="micro-kpi-lbl">Brecha de Edad Media · +13 años en NO ATP</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">68,95%</span>
          <span class="micro-kpi-lbl">Madurez Productiva ATP · 41-65 años (131 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val noatp-text">52,49%</span>
          <span class="micro-kpi-lbl">Edad de Jubilación NO ATP · >65 años (527 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">17,4% vs 5,2%</span>
          <span class="micro-kpi-lbl">Tasa de Juventud · 18-40 años (Triple en ATP)</span>
        </div>
      </div>"""

new_sec5_kpis = """      <!-- Micro-KPIs Resumen Edad y Relevo -->
      <div class="micro-kpi-grid">
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">53 vs 66</span>
          <span class="micro-kpi-lbl">Brecha de Edad Media · +13 años en NO ATP</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">72,63%</span>
          <span class="micro-kpi-lbl">Madurez Productiva ATP · 41-65 años (138 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val noatp-text">74,20%</span>
          <span class="micro-kpi-lbl">Edad de Jubilación NO ATP · >65 años (745 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">17,4% vs 5,8%</span>
          <span class="micro-kpi-lbl">Tasa de Juventud · 18-40 años (Triple en ATP)</span>
        </div>
      </div>"""

content = content.replace(old_sec5_kpis, new_sec5_kpis)

# Replace alert box in NO ATP
old_alert_box = """              <div class="pill-summary-box summary-amber" style="margin-top: 14px; border-left: 3px solid #DC2626;">
                <strong style="color: #DC2626;">Alerta Demográfica:</strong> <strong>527 mujeres (52,5%) superan los 65 años</strong>. Más de la mitad de las explotaciones comerciales no profesionales afrontan riesgo inminente de cese en esta década por falta de relevo tutelado.
              </div>"""

new_alert_box = """              <div class="pill-summary-box summary-amber" style="margin-top: 14px; border-left: 3px solid #DC2626;">
                <strong style="color: #DC2626;">Alerta Demográfica:</strong> <strong>745 mujeres (74,2%) superan los 65 años</strong> (frente al 60,5% de los hombres). Casi tres de cada cuatro explotaciones comerciales no profesionales afrontan riesgo inminente de cese en esta década por jubilación sin relevo tutelado.
              </div>"""

content = content.replace(old_alert_box, new_alert_box)

# Replace bottom insight card in Section 5
old_insight_sec5 = """Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>más de la mitad de las mujeres (52,5% - 527 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,2%. Sin un plan de relevo tutelado, más de 500 explotaciones corren riesgo de cese en la presente década."""

new_insight_sec5 = """Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>casi tres de cada cuatro mujeres (74,2% - 745 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,8% (58 mujeres). Sin un plan de relevo tutelado, más de 700 explotaciones corren riesgo de cese en la presente década."""

content = content.replace(old_insight_sec5, new_insight_sec5)

# 3. Update DATA_EXCEL
# Replace No_ATP marco general and edad
old_noatp_data = """"marco_general": {
          "total_explotaciones": 12120,
          "hombres_total": 8458,
          "hombres_pct": 69.79,
          "mujeres_total": 3662,
          "mujeres_pct": 30.21,
          "autoconsumo": {
            "total": 8798,
            "hombres": 6330,
            "mujeres": 2468,
            "pct_h": 52.23,
            "pct_m": 20.36
          },
          "fines_mercado": {
            "total": 3322,
            "hombres": 2128,
            "mujeres": 1194,
            "pct_h": 17.56,
            "pct_m": 9.85
          },
          "no_atp_mercado": {
            "total": 2793,
            "hombres": 1789,
            "mujeres": 1004
          }
        },
        "edad": {
          "edad_media": {
            "hombres": 60,
            "mujeres": 66
          },
          "tramos": [
            {"tramo": "18-40", "h": 185, "m": 52, "h_pct": 6.62, "m_pct": 1.86, "m_pct_sobre_m": 5.18},
            {"tramo": "41-65", "h": 945, "m": 425, "h_pct": 33.83, "m_pct": 15.22, "m_pct_sobre_m": 42.33},
            {"tramo": "Mayor de 65", "h": 659, "m": 527, "h_pct": 23.59, "m_pct": 18.87, "m_pct_sobre_m": 52.49}
          ]
        },"""

new_noatp_data = """"marco_general": {
          "total_explotaciones": 12126,
          "hombres_total": 8462,
          "hombres_pct": 69.78,
          "mujeres_total": 3664,
          "mujeres_pct": 30.22,
          "autoconsumo": {
            "total": 8805,
            "hombres": 6335,
            "mujeres": 2470,
            "pct_h": 52.24,
            "pct_m": 20.37
          },
          "fines_mercado": {
            "total": 3323,
            "hombres": 2129,
            "mujeres": 1194,
            "pct_h": 17.56,
            "pct_m": 9.85
          },
          "no_atp_mercado": {
            "total": 2793,
            "hombres": 1789,
            "mujeres": 1004
          }
        },
        "edad": {
          "edad_media": {
            "hombres": 60,
            "mujeres": 66
          },
          "tramos": [
            {"tramo": "18-40", "h": 209, "m": 58, "h_pct": 11.69, "m_pct_sobre_m": 5.78},
            {"tramo": "41-65", "h": 500, "m": 201, "h_pct": 27.96, "m_pct_sobre_m": 20.02},
            {"tramo": "Mayor de 65", "h": 1081, "m": 745, "h_pct": 60.46, "m_pct_sobre_m": 74.20}
          ]
        },"""

content = content.replace(old_noatp_data, new_noatp_data)

# Replace ATP edad
old_atp_edad = """"edad": {
          "edad_media_m": 53,
          "tramos": [
            {"tramo": "18-40", "h": 80, "m": 33, "m_pct_sobre_m": 17.37},
            {"tramo": "41-65", "h": 227, "m": 131, "m_pct_sobre_m": 68.95},
            {"tramo": "Mayor de 65", "h": 23, "m": 26, "m_pct_sobre_m": 13.68}
          ]
        },"""

new_atp_edad = """"edad": {
          "edad_media_m": 53,
          "tramos": [
            {"tramo": "18-40", "h": 80, "m": 33, "h_pct": 24.24, "m_pct_sobre_m": 17.37},
            {"tramo": "41-65", "h": 227, "m": 138, "h_pct": 68.79, "m_pct_sobre_m": 72.63},
            {"tramo": "Mayor de 65", "h": 23, "m": 19, "h_pct": 6.97, "m_pct_sobre_m": 10.00}
          ]
        },"""

content = content.replace(old_atp_edad, new_atp_edad)

# 4. Update renderEdad()
old_render_edad = """    // 6. RENDER EDAD
    function renderEdad() {
      const atpList = document.getElementById('list-edad-atp');
      const noatpList = document.getElementById('list-edad-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct atp-pct">17,37% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(33 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 80 (%24,24)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 17.37%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct atp-pct">68,95% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(131 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 227 (%68,79)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 68.95%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageOld}</span>
            <span class="segment-item-pct atp-pct">13,68% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(26 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 23 (%6,97)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 13.68%;"></div></div>
        </div>
      `;

      noatpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct noatp-pct">5,18% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(52 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 185 (%10,34)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 5.18%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct noatp-pct">42,33% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(425 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 945 (%52,82)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 42.33%;"></div></div>
        </div>
        <div class="segment-item" style="border-color: #FECACA; background: #FEF2F2;">
          <div class="segment-item-top">
            <span class="segment-item-name" style="color: #991B1B;">${t.ageOldAlert}</span>
            <span class="segment-item-pct" style="color: #DC2626;">52,49% <span style="font-size:11px;font-weight:500;color:#991B1B;">(527 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 659 (%36,84)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 52.49%; background: #DC2626;"></div></div>
        </div>
      `;
    }"""

new_render_edad = """    // 6. RENDER EDAD
    function renderEdad() {
      const atpList = document.getElementById('list-edad-atp');
      const noatpList = document.getElementById('list-edad-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct atp-pct">17,37% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(33 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 80 (24,24%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 17.37%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct atp-pct">72,63% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(138 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 227 (68,79%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 72.63%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageOld}</span>
            <span class="segment-item-pct atp-pct">10,00% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(19 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} ATP: 23 (6,97%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 10.00%;"></div></div>
        </div>
      `;

      noatpList.innerHTML = `
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageYoung}</span>
            <span class="segment-item-pct noatp-pct">5,78% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(58 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 209 (11,69%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 5.78%;"></div></div>
        </div>
        <div class="segment-item">
          <div class="segment-item-top">
            <span class="segment-item-name">${t.ageMid}</span>
            <span class="segment-item-pct noatp-pct">20,02% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(201 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 500 (27,96%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: 20.02%;"></div></div>
        </div>
        <div class="segment-item" style="border-color: #FECACA; background: #FEF2F2;">
          <div class="segment-item-top">
            <span class="segment-item-name" style="color: #991B1B;">${t.ageOldAlert}</span>
            <span class="segment-item-pct" style="color: #DC2626;">74,20% <span style="font-size:11px;font-weight:500;color:#991B1B;">(745 ${mLabel})</span></span>
          </div>
          <div class="segment-item-sub">${t.hombresPrefix} EZ-ATP: 1.081 (60,46%)</div>
          <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 74.20%; background: #DC2626;"></div></div>
        </div>
      `;
    }"""

content = content.replace(old_render_edad, new_render_edad)

# 5. Update I18N texts
content = content.replace(
    '"kpi1Desc": "3.662 Mujeres (30,2%) | 8.458 Hombres"',
    '"kpi1Desc": "3.664 Mujeres (30,2%) | 8.462 Hombres"'
)
content = content.replace(
    '"kpi2Desc": "1.194 Mujeres (35,9%) | 2.128 Hombres"',
    '"kpi2Desc": "1.194 Mujeres (35,9%) | 2.129 Hombres"'
)
content = content.replace(
    '"kpi1Desc": "3.662 Emakume (%30,2) | 8.458 Gizon"',
    '"kpi1Desc": "3.664 Emakume (%30,2) | 8.462 Gizon"'
)
content = content.replace(
    '"kpi2Desc": "1.194 Emakume (%35,9) | 2.128 Gizon"',
    '"kpi2Desc": "1.194 Emakume (%35,9) | 2.129 Gizon"'
)
content = content.replace(
    '"sec6InsightText": "Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>más de la mitad de las mujeres (52,5% - 527 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,2%. Sin un plan de relevo tutelado, más de 500 explotaciones corren riesgo de cese en la presente década."',
    '"sec6InsightText": "Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>casi tres de cada cuatro mujeres (74,2% - 745 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,8% (58 mujeres). Sin un plan de relevo tutelado, más de 700 explotaciones corren riesgo de cese en la presente década."'
)
content = content.replace(
    '"sec6InsightText": "Belaunaldi-arrakala handia dago, <strong>13 urteko aldearekin batez besteko adinean</strong> (53 urte ATPn eta 66 urte Ez-ATPn). Ez-ATP taldean, <strong>emakumeen erdiak baino gehiagok (%52,5 - 527 titular) erretiratzeko adin ofiziala gainditzen du</strong>; 40 urtetik beherakoak, berriz, apenas dira %5,2. Errelebo-planik gabe, 500 ustiategi baino gehiago desagertzeko arriskuan daude hamarkada honetan."',
    '"sec6InsightText": "Belaunaldi-arrakala handia dago, <strong>13 urteko aldearekin batez besteko adinean</strong> (53 urte ATPn eta 66 urte Ez-ATPn). Ez-ATP taldean, <strong>emakumeen ia hiru laurdenak (%74,2 - 745 titular) erretiratzeko adin ofiziala gainditzen du</strong>; 40 urtetik beherakoak, berriz, apenas dira %5,8 (58 emakume). Errelebo-planik gabe, 700 ustiategi baino gehiago desagertzeko arriskuan daude hamarkada honetan."'
)

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synchronized all tables and texts to official Excel document 20260925_DatosExplotaciones.xlsx!")
