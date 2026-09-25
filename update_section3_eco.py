# update_section3_eco.py
new_sec3_html = """    <!-- BLOQUE 3: ECOLÓGICO (EXCLUSIVO ATP) -->
    <section class="block-section" id="bloque-ecologico">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-tag" id="txt-sec3-tag">INDICADOR ESTRUCTURAL 3</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M12 2a10 10 0 0 0-10 10c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
            </svg>
            <span id="txt-sec3-title">Sostenibilidad y Producción Ecológica Oficial (ATP)</span>
          </h2>
          <p class="section-desc" id="txt-sec3-desc">
            Análisis de la <strong>producción ecológica en las mujeres profesionales ATP</strong> (certificado, parcial y en proceso de certificación). El colectivo No ATP se excluye del cómputo ecológico según las directrices forales.
          </p>
        </div>
        <div class="section-badge-group">
          <span class="badge badge-atp" id="badge-atp-pill-3">ATP: 190 Mujeres</span>
        </div>
      </div>

      <!-- Micro-KPIs Resumen Ecológico ATP -->
      <div class="micro-kpi-grid">
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">11,58%</span>
          <span class="micro-kpi-lbl">Tasa Eco Mujeres ATP · 22 de 190</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">12% vs 9%</span>
          <span class="micro-kpi-lbl">Mayor Vocación Eco · Mujeres vs Hombres</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">40,7%</span>
          <span class="micro-kpi-lbl">Cuota Femenina · 22 de 54 eco Bizkaia</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">17 de 22</span>
          <span class="micro-kpi-lbl">Certificado Oficial Pleno · 8,95% del total</span>
        </div>
      </div>

      <!-- Tarjeta Principal con Estructura Bipartita Lado a Lado -->
      <div class="card card-atp col-atp" style="border-top: 4px solid var(--atp-primary); margin-bottom: 24px;">
        <div class="card-header">
          <div class="card-title">
            <span class="badge badge-atp">ATP</span>
            <span id="txt-sec3-atp-card-title">Certificaciones y Grado de Conversión Ecológica</span>
          </div>
          <span class="card-subtext" id="txt-sec3-atp-base">Base: 190 Mujeres ATP (22 en producción ecológica)</span>
        </div>

        <div class="atp-subsector-split" style="grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));">
          <!-- Columna Izquierda: Datos y Barras -->
          <div class="atp-subsector-data">
            <div class="metric-hero">
              <span class="metric-val atp-text">11,58%</span>
              <span class="metric-unit" id="txt-sec3-atp-unit">con actividad ecológica (22 mujeres)</span>
            </div>
            <p style="font-size: 13.5px; color: var(--slate-600); margin-bottom: 16px; line-height: 1.5;" id="txt-sec3-atp-text">
              De las 22 mujeres ecológicas ATP: <strong>17 disponen de certificado oficial</strong> (8,95%), 4 certifican una parte (2,11%) y 1 está en proceso (0,53%).
            </p>

            <div class="segment-list" id="list-ecologico-atp"></div>

            <div class="pill-summary-box summary-emerald" style="margin-top: 18px;" id="txt-sec3-atp-note">
              <strong>Liderazgo femenino en el sector eco ATP:</strong> Las 22 mujeres representan el <strong>40,7% de todas las explotaciones ecológicas profesionales</strong> de Bizkaia (54 en total: 32 hombres y 22 mujeres), superando claramente su peso relativo en el censo agrario general (35,9%).
            </div>
          </div>

          <!-- Columna Derecha: Análisis Oficial Celda N39 -->
          <div class="atp-subsector-narrative">
            <div class="insight-pill-card pill-emerald">
              <div class="pill-header">
                <span class="pill-tag tag-emerald">1. Vocación Productiva por Género</span>
                <h4 class="pill-title">Mayor Tasa de Conversión Ecológica en Mujeres</h4>
              </div>
              <div class="pill-body">
                <p>El <strong>12% de las mujeres ATP produce en ecológico</strong>, frente al <strong>9% de los hombres</strong>.</p>
                <p>Este dato refleja una orientación prioritaria hacia modelos de alto valor añadido, respeto medioambiental y circuitos cortos de comercialización dentro del perfil profesional femenino.</p>
              </div>
            </div>

            <div class="insight-pill-card pill-emerald" style="border-top: 3px solid #059669;">
              <div class="pill-header">
                <span class="pill-tag tag-emerald">2. Representatividad Sectorial</span>
                <h4 class="pill-title">Sobrerrepresentación Femenina en la Producción Sostenible</h4>
              </div>
              <div class="pill-body">
                <p>Las mujeres representan el <strong>41% de las personas ATP que producen en ecológico</strong>, frente al <strong>36%</strong> que representan en el conjunto de ATP.</p>
                <div class="pill-summary-box summary-emerald">
                  <strong>Clave para la Infografía:</strong> La presencia femenina en la producción agroecológica profesional (41%) supera en 5 puntos porcentuales su peso en el censo agrario foral (36%), consolidándose como protagonistas de la sostenibilidad agraria en Bizkaia.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
"""

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- BLOQUE 3: ECOL'
start_idx = html.find(start_marker)
start_line_idx = html.rfind('\n', 0, start_idx) + 1

end_marker = '    <!-- BLOQUE 4: COMARCAS -->'
end_line_idx = html.find(end_marker)

assert start_line_idx != -1 and end_line_idx != -1, f"Indices: {start_line_idx}, {end_line_idx}"

updated_html = html[:start_line_idx] + new_sec3_html + '\n' + html[end_line_idx:]

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Bloque 3 successfully re-updated with proper micro-kpi-val and bipartite grid!")
