# update_sec3_data.py
import re

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Bloque 3 Micro KPI box 4
content = content.replace(
    """        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">17 de 22</span>
          <span class="micro-kpi-lbl">Certificado Oficial Pleno · 8,95% del total</span>
        </div>""",
    """        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">54 Proyectos</span>
          <span class="micro-kpi-lbl">Total Agroecológico ATP · 22 m. y 32 h.</span>
        </div>"""
)

# 2. Update descriptive paragraph
content = content.replace(
    """            <p style="font-size: 13.5px; color: var(--slate-600); margin-bottom: 16px; line-height: 1.5;" id="txt-sec3-atp-text">
              De las 22 mujeres ecológicas ATP: <strong>17 disponen de certificado oficial</strong> (8,95%), 4 certifican una parte (2,11%) y 1 está en proceso (0,53%).
            </p>""",
    """            <p style="font-size: 13.5px; color: var(--slate-600); margin-bottom: 16px; line-height: 1.5;" id="txt-sec3-atp-text">
              Un total de <strong>22 mujeres profesionales ATP (11,58%)</strong> gestionan explotaciones con certificación ecológica oficial en Bizkaia, frente a <strong>32 hombres (9,44%)</strong>.
            </p>"""
)

# 3. Update DATA_EXCEL.ATP.ecologico
old_eco_data = """"ecologico": [
          {"tipo": "Certificado ecológico", "h": 24, "m": 17, "pct_m_de_190": 8.95},
          {"tipo": "Una parte de la explotación", "h": 4, "m": 4, "pct_m_de_190": 2.11},
          {"tipo": "En proceso de certificación", "h": 4, "m": 1, "pct_m_de_190": 0.53}
        ],"""

new_eco_data = """"ecologico": [
          {"tipo": "Certificado ecológico", "h": 32, "m": 22, "pct_m_de_190": 11.58}
        ],"""

content = content.replace(old_eco_data, new_eco_data)

# 4. Update renderEcologico
old_render_eco = """    // 3. RENDER ECOLOGICO
    function renderEcologico() {
      const atpList = document.getElementById('list-ecologico-atp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      if (atpList) {
        atpList.innerHTML = '';
        DATA_EXCEL.ATP.ecologico.forEach(e => {
          atpList.innerHTML += `
            <div class="segment-item">
              <div class="segment-item-top">
                <span class="segment-item-name">${translateName(e.tipo)}</span>
                <span class="segment-item-pct atp-pct">${e.pct_m_de_190}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${e.m} ${mLabel})</span></span>
              </div>
              <div class="segment-item-sub">${t.hombresPrefix}: ${e.h} | ${t.mujeresPrefix}: ${e.m}</div>
              <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: ${e.pct_m_de_190 * 8}%;"></div></div>
            </div>
          `;
        });
      }
    }"""

new_render_eco = """    // 3. RENDER ECOLOGICO
    function renderEcologico() {
      const atpList = document.getElementById('list-ecologico-atp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      if (atpList) {
        atpList.innerHTML = `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${CURRENT_LANG === 'eu' ? 'Ziurtagiri Ekologiko Ofiziala' : 'Certificado Ecológico Oficial'}</span>
              <span class="segment-item-pct atp-pct">11,58% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(22 ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix} ATP: 32 (9,44%) | ${t.mujeresPrefix} ATP: 22 (11,58%)</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 11.58%;"></div></div>
          </div>
          <div class="segment-item" style="background: #F0FDF4; border: 1px solid #BBF7D0; margin-top: 10px;">
            <div class="segment-item-top">
              <span class="segment-item-name" style="font-weight:700; color: #166534;">${CURRENT_LANG === 'eu' ? 'Emakumeen Pisua Ekoizpen Ekologikoan Guztira' : 'Cuota Femenina en la Producción Ecológica Profesional'}</span>
              <span class="segment-item-pct atp-pct" style="color: #047857;">40,74% <span style="font-size:11px;font-weight:600;color:#15803D;">(22 / 54)</span></span>
            </div>
            <div class="segment-item-sub" style="color: #15803D;">${CURRENT_LANG === 'eu' ? '54 ustiategi ekologiko guztira Bizkaian (32 gizon eta 22 emakume)' : '54 explotaciones ecológicas profesionales en Bizkaia (32 hombres y 22 mujeres)'}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-atp" style="width: 40.74%;"></div></div>
          </div>
        `;
      }
    }"""

content = content.replace(old_render_eco, new_render_eco)

# 5. Update I18N texts for Sec3
content = content.replace(
    '"sec3AtpText": "De las 22 mujeres ecológicas ATP: <strong>17 disponen de certificado oficial</strong> (8,95%), 4 certifican una parte (2,11%) y 1 está en proceso (0,53%)."',
    '"sec3AtpText": "Un total de <strong>22 mujeres profesionales ATP (11,58%)</strong> gestionan explotaciones con certificación ecológica oficial en Bizkaia, frente a <strong>32 hombres (9,44%)</strong>."'
)
content = content.replace(
    '"sec3AtpText": "ATPko 22 emakume ekologikoetatik: <strong>17k ziurtagiri ofiziala dute</strong> (%8,95), 4k zati bat (%2,11) eta 1 prozesuan dago (%0,53)."',
    '"sec3AtpText": "ATP profesionaletako <strong>22 emakumek (%11,58)</strong> ziurtagiri ekologiko ofiziala duten ustiategiak kudeatzen dituzte Bizkaian, <strong>32 gizonen (%9,44)</strong> aldean."'
)

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Bloque 3 Ecológico synced with exact Excel sheet ATP row 40!")
