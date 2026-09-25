# -*- coding: utf-8 -*-
"""
Redesign Block 2 (Dimensión y Superficie) in reporte_diputacion_agro_2.html:
- ATP: Remove 'Comentario Oficial ATP (Celda L34)', add micro-KPIs, bipartite layout, structured insight pills.
- NO ATP: Remove 'Comentario Oficial NO ATP (Celda J56)', add micro-KPIs, bipartite layout, structured insight pills.
- Protect setLang assignments from overwriting rich layout.
"""
import re

def update_section2():
    with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    new_sec2_dual_grid = """      <div class="dual-grid">
        <!-- COL ATP SUPERFICIE -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span id="txt-sec2-atp-card-title">Superficie en Mujeres Profesionales</span>
            </div>
            <span class="card-subtext" id="txt-sec2-atp-base">Base: 190 Mujeres ATP</span>
          </div>

          <!-- Micro KPIs ATP Superficie -->
          <div class="micro-kpi-grid">
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">67,9%</span>
              <span class="micro-kpi-lbl">Bases Viables (> 5 ha - 129 m.)</span>
            </div>
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">59,5%</span>
              <span class="micro-kpi-lbl">Menos de 20 ha (113 m.)</span>
            </div>
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">40,5%</span>
              <span class="micro-kpi-lbl">Mediana o Grande (> 20 ha)</span>
            </div>
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">14,2%</span>
              <span class="micro-kpi-lbl">Grande (> 50 ha) vs 24% H</span>
            </div>
          </div>

          <!-- Estructura Bipartita ATP -->
          <div class="atp-subsector-split">
            <!-- Zona Izquierda: Datos y Estratos -->
            <div class="atp-subsector-data">
              <div class="subsector-side-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
                Estratos de Superficie (ATP)
              </div>
              <div class="segment-list" id="list-superficie-atp"></div>
            </div>

            <!-- Zona Derecha: Píldoras de Análisis Narrativo L34 -->
            <div class="atp-subsector-narrative" id="txt-sec2-atp-text">
              <div class="insight-pill-card pill-emerald">
                <div class="pill-header">
                  <span class="pill-tag tag-emerald">Estructura Dimensional</span>
                  <h4 class="pill-title">Distribución según Escala y Diferencias de Género</h4>
                </div>
                <div class="pill-body">
                  <p>La distribución de las explotaciones según su superficie muestra diferencias entre mujeres y hombres ATP. En el caso de las mujeres, más de la mitad (<strong>59%</strong>) gestiona explotaciones de menos de 20 hectáreas: un <strong>32%</strong> corresponde a explotaciones de entre 0,5 y 5 hectáreas y un <strong>27%</strong> a explotaciones de entre 5 y 20 hectáreas.</p>
                  <p>Entre los hombres ATP, el 50% se concentra también en explotaciones de menos de 20 hectáreas, aunque con una distribución diferente: el <strong>33%</strong> gestiona de 0,5 a 5 hectáreas y el <strong>17%</strong> explotaciones de 5 a 20 hectáreas.</p>
                </div>
              </div>

              <div class="insight-pill-card pill-emerald" style="border-top: 3px solid #047857;">
                <div class="pill-header">
                  <span class="pill-tag tag-emerald">Brecha en Grandes Fincas</span>
                  <h4 class="pill-title">Concentración en Fincas Superiores a 20 Hectáreas</h4>
                </div>
                <div class="pill-body">
                  <p>A partir de las 20 hectáreas, el peso relativo de las explotaciones es mayor entre los hombres: representan el <strong>50% de sus explotaciones, frente al 41% entre las mujeres</strong>.</p>
                  <p>La diferencia es especialmente significativa en las explotaciones de <strong>más de 50 hectáreas</strong>, que suponen el <strong>24% entre los hombres y el 14% entre las mujeres</strong>.</p>
                  <div class="pill-summary-box summary-emerald">
                    <strong>Conclusión:</strong> Las mujeres ATP presentan una mayor concentración relativa en explotaciones de menos de 20 hectáreas, mientras que entre los hombres tiene mayor peso la gestión de fincas de gran escala (>50 ha).
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COL NO ATP SUPERFICIE -->
        <div class="card card-noatp col-noatp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-noatp">NO ATP</span>
              <span id="txt-sec2-noatp-card-title">Superficie en Explotaciones Comerciales</span>
            </div>
            <span class="card-subtext" id="txt-sec2-noatp-base">Base: 1.004 Mujeres No ATP</span>
          </div>

          <!-- Micro KPIs NO ATP Superficie -->
          <div class="micro-kpi-grid">
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">74,6%</span>
              <span class="micro-kpi-lbl">Minifundio (&lt; 5 ha - 749 m.)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">19,8%</span>
              <span class="micro-kpi-lbl">Pequeña (5 - 20 ha - 199 m.)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">5,0%</span>
              <span class="micro-kpi-lbl">Mediana (20 - 50 ha - 50 m.)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">0,6%</span>
              <span class="micro-kpi-lbl">Grande (> 50 ha - solo 6 m.)</span>
            </div>
          </div>

          <!-- Estructura Bipartita NO ATP -->
          <div class="atp-subsector-split">
            <!-- Zona Izquierda: Datos y Estratos -->
            <div class="atp-subsector-data">
              <div class="subsector-side-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
                Estratos de Superficie (NO ATP)
              </div>
              <div class="segment-list" id="list-superficie-noatp"></div>
            </div>

            <!-- Zona Derecha: Píldoras de Análisis Narrativo J56 -->
            <div class="atp-subsector-narrative" id="txt-sec2-noatp-text">
              <div class="insight-pill-card pill-amber">
                <div class="pill-header">
                  <span class="pill-tag tag-amber">Patrón de Minifundio</span>
                  <h4 class="pill-title">Predominio de Pequeñas Dimensiones en Ambos Géneros</h4>
                </div>
                <div class="pill-body">
                  <p>La distribución por superficie es muy similar entre hombres y mujeres NO ATP. En ambos casos predominan claramente las explotaciones muy pequeñas, de <strong>0,5 a 5 hectáreas, que representan el 69% de los hombres y el 75% de las mujeres</strong>.</p>
                  <p>A medida que aumenta la superficie, el peso disminuye rápidamente en ambos géneros: las fincas de 5 a 20 ha suponen el <strong>23% de los hombres y el 20% de las mujeres</strong>, mientras que las de 20 a 50 ha apenas alcanzan el <strong>6% y 5%</strong>, respectivamente.</p>
                </div>
              </div>

              <div class="insight-pill-card pill-amber" style="border-top: 3px solid #D97706;">
                <div class="pill-header">
                  <span class="pill-tag tag-amber">Gran Escala Testimonial</span>
                  <h4 class="pill-title">Escasa Presencia en Superficies Superiores a 50 Hectáreas</h4>
                </div>
                <div class="pill-body">
                  <p>Las explotaciones de más de 50 ha tienen un peso extraordinariamente reducido: <strong>2% entre los hombres y solo un 1% entre las mujeres</strong> (apenas 6 titulares en toda la provincia de Bizkaia).</p>
                  <div class="pill-summary-box summary-amber">
                    <strong>Conclusión:</strong> En el modelo NO ATP comercial, 3 de cada 4 mujeres no alcanzan las 5 hectáreas, reflejando una fragmentación territorial estructural que limita la mecanización y el aprovechamiento de pastos forrajeros.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>"""

    # Locate and replace old dual-grid in Section 2
    sec2_dual_pattern = r'(<section class="block-section" id="bloque-superficie">.*?)(<div class="dual-grid">.*?</div>\s*</div>\s*</div>\s*)(<div class="insight-card">)'
    m = re.search(sec2_dual_pattern, html, re.DOTALL)
    if m:
        html = html[:m.start(2)] + new_sec2_dual_grid + '\n\n      ' + html[m.start(3):]
        print("Replaced Section 2 dual grid successfully!")
    else:
        # Fallback locate
        m_fallback = re.search(r'(<!-- COL ATP SUPERFICIE -->.*?)(<div class="insight-card">)', html, re.DOTALL)
        if m_fallback:
            # find opening <div class="dual-grid"> right before it
            pos_open = html.rfind('<div class="dual-grid">', 0, m_fallback.start(1))
            html = html[:pos_open] + new_sec2_dual_grid + '\n\n      ' + html[m_fallback.start(2):]
            print("Replaced Section 2 dual grid via fallback!")
        else:
            print("ERROR: Could not locate Section 2 dual grid!")
            return False

    # Protect sec2 from setLang overwrite
    html = html.replace(
        "document.getElementById('txt-sec2-atp-text').innerHTML = t.sec2AtpText;\n      document.getElementById('txt-sec2-noatp-text').innerHTML = t.sec2NoatpText;",
        "// document.getElementById('txt-sec2-atp-text').innerHTML = t.sec2AtpText;\n      // document.getElementById('txt-sec2-noatp-text').innerHTML = t.sec2NoatpText;"
    )

    with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Updated Section 2 in reporte_diputacion_agro_2.html successfully.")
    return True

if __name__ == '__main__':
    update_section2()
