# -*- coding: utf-8 -*-
"""
Update Block 1 (NO ATP Subsectores) in reporte_diputacion_agro_2.html:
- Eliminates technical labels like 'Comentario Oficial NO ATP (Celda J32)'.
- Implements an editorial bipartite structure (Left: Data/Ranking/Table, Right: Structured Insights with micro-badges and conclusions).
- Adds top micro-KPI summary row (44,6% Bovino Carne, 12,2% Ovinos, 10,4% No Clasificadas, 7,8% Huerta Aire Libre).
- Harmonizes with the ATP card in Dual View and Solo NO ATP view.
"""
import re

def update_block_1_noatp():
    with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add extra CSS styles for amber/NO ATP theme
    amber_css = """
    /* --- ESTILOS AMBER PARA NO ATP SUBSECTORES --- */
    @media (min-width: 1100px) {
      body.mode-noatp-only .atp-subsector-split {
        grid-template-columns: 1.02fr 1.18fr;
        gap: 28px;
        align-items: start;
      }
    }
    .micro-kpi-box.kpi-amber {
      background: #FFFBEB;
      border-color: #FDE68A;
    }
    .micro-kpi-box.kpi-amber .micro-kpi-val {
      color: #B45309;
    }
    .insight-pill-card.pill-amber {
      background: #FFFDF5;
      border-color: #FDE68A;
    }
    .pill-tag.tag-amber {
      background: #D97706;
      color: #FFFFFF;
    }
    .pill-summary-box.summary-amber {
      background: rgba(217, 119, 6, 0.08);
      border-left: 3px solid #D97706;
      color: #78350F;
    }
    .paridad-item.paridad-amber {
      border-color: rgba(253, 230, 138, 0.7);
      background: rgba(255, 255, 255, 0.85);
    }
    .paridad-badge.badge-amber {
      background: #FEF3C7;
      color: #92400E;
    }
"""
    if '/* --- ESTILOS AMBER PARA NO ATP SUBSECTORES --- */' not in html:
        html = html.replace('</style>', amber_css + '\n  </style>')

    # 2. Build the new NO ATP card for Section 1
    new_noatp_card = """        <!-- COL NO ATP SUBSECTORES -->
        <div class="card card-noatp col-noatp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-noatp">NO ATP</span>
              <span id="txt-sec1-noatp-card-title">Subsectores en Explotaciones Comerciales</span>
            </div>
            <span class="card-subtext" id="txt-sec1-noatp-base">Base: 1.004 Mujeres No ATP (100%)</span>
          </div>

          <!-- Micro KPIs de síntesis sectorial NO ATP -->
          <div class="micro-kpi-grid">
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">44,6%</span>
              <span class="micro-kpi-lbl">Bovino Carne (448 mujeres)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">12,2%</span>
              <span class="micro-kpi-lbl">Ovinos (122 mujeres)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">10,4%</span>
              <span class="micro-kpi-lbl">No Clasificadas (104 mujeres)</span>
            </div>
            <div class="micro-kpi-box kpi-amber">
              <span class="micro-kpi-val">7,8%</span>
              <span class="micro-kpi-lbl">Huerta Aire Libre (78 mujeres)</span>
            </div>
          </div>

          <!-- Estructura Bipartita: Datos a la izquierda / Análisis cualitativo a la derecha -->
          <div class="atp-subsector-split">
            <!-- Zona Izquierda: Datos y Ranking Top 5 -->
            <div class="atp-subsector-data">
              <div class="subsector-side-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                Ranking de Actividad Comercial Femenina
              </div>

              <div class="segment-list" id="list-subsectores-noatp"></div>

              <button class="btn-toggle-expand" onclick="toggleExpand('table-subsectores-noatp', this)" style="margin-top: 14px;">
                <span id="txt-sec1-noatp-btn">Mostrar tabla completa de 18 subsectores NO ATP</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </button>

              <div id="table-subsectores-noatp" class="table-responsive" style="display: none; margin-top: 12px;">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th id="th-sub-noatp-name">Subsector</th>
                      <th class="num" id="th-sub-noatp-h">Hombres</th>
                      <th class="num" id="th-sub-noatp-m">Mujeres</th>
                      <th class="num" id="th-sub-noatp-pct">% Mujeres (de 1004)</th>
                    </tr>
                  </thead>
                  <tbody id="tbody-subsectores-noatp"></tbody>
                </table>
              </div>
            </div>

            <!-- Zona Derecha: Píldoras de Hallazgos y Análisis Narrativo -->
            <div class="atp-subsector-narrative" id="txt-sec1-noatp-text">
              <!-- Píldora 1: Concentración en Bovino de Carne -->
              <div class="insight-pill-card pill-amber">
                <div class="pill-header">
                  <span class="pill-tag tag-amber">Patrón Productivo Mayoritario</span>
                  <h4 class="pill-title">Concentración en Vacuno de Carne y Estructura por Género</h4>
                </div>
                <div class="pill-body">
                  <p>Entre las personas NO ATP con fines de mercado, tanto hombres como mujeres se concentran principalmente en las explotaciones de <strong>bovinos especializadas en orientación cría y carne</strong>, que representan el <strong>44% de los hombres y el 45% de las mujeres</strong>.</p>
                  <p>A bastante distancia, entre las mujeres destacan las explotaciones de <strong>ovinos (12%)</strong>, las <strong>no clasificadas (10%)</strong> y las <strong>hortalizas al aire libre (8%)</strong>. Entre los hombres, tras el vacuno de carne destacan también las explotaciones de ovinos (12%), las no clasificadas (10%) y las hortalizas al aire libre (6%).</p>
                  <p>En el resto de subsectores, el peso es más reducido, sin superar el 6% ni entre las mujeres ni entre los hombres.</p>
                  <div class="pill-summary-box summary-amber">
                    <strong>Conclusión:</strong> El vacuno de carne vertebra la actividad de casi la mitad de los titulares en ambos géneros, con una estructura proporcional prácticamente idéntica entre hombres y mujeres.
                  </div>
                </div>
              </div>

              <!-- Píldora 2: Claves para la Infografía y Segundas Actividades -->
              <div class="insight-pill-card pill-amber" style="border-top: 3px solid #D97706;">
                <div class="pill-header">
                  <span class="pill-tag tag-amber">Claves para la Infografía</span>
                  <h4 class="pill-title">Jerarquía Sectorial y Datos Destacados</h4>
                </div>
                <div class="pill-body">
                  <div class="paridad-list">
                    <div class="paridad-item paridad-amber">
                      <span class="paridad-badge badge-amber">Dato Principal</span>
                      <div>El <strong>45% de las mujeres</strong> y el <strong>44% de los hombres</strong> NO ATP con fines de mercado se concentran en <strong>bovinos de cría y carne</strong>.</div>
                    </div>
                    <div class="paridad-item paridad-amber">
                      <span class="paridad-badge badge-amber">Segundo Dato</span>
                      <div><strong>Ovinos (12%)</strong> y <strong>explotaciones no clasificadas (10%)</strong> son los siguientes subsectores con mayor peso en ambos géneros.</div>
                    </div>
                    <div class="paridad-item paridad-amber">
                      <span class="paridad-badge badge-amber">Huerta Tradicional</span>
                      <div>Las <strong>hortalizas al aire libre</strong> alcanzan el <strong>8% en mujeres</strong> (frente al 6% en hombres), consolidándose como la cuarta orientación productiva.</div>
                    </div>
                  </div>

                  <div class="pill-summary-box summary-amber">
                    <strong>Contraste con el segmento ATP:</strong> En el modelo No ATP comercial, la ganadería ovina extensiva y la huerta al aire libre reemplazan la fuerte presencia que en ATP tienen el vacuno de leche (13,2%) y los invernaderos tecnificados (8,9%).
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>"""

    # Locate and replace old NO ATP card in Section 1
    m = re.search(r'(<!-- COL NO ATP SUBSECTORES -->\s*<div class="card card-noatp col-noatp">.*?)(<!-- Analytical Key Takeaway -->)', html, re.DOTALL)
    if m:
        html = html[:m.start(1)] + new_noatp_card + '\n\n      ' + html[m.start(2):]
        print("Replaced NO ATP subsector card successfully!")
    else:
        print("ERROR: Could not locate COL NO ATP SUBSECTORES!")
        return False

    # 3. Protect txt-sec1-noatp-text from overwrite in setLang
    html = html.replace(
        "document.getElementById('txt-sec1-noatp-text').innerHTML = t.sec1NoatpText;",
        "// document.getElementById('txt-sec1-noatp-text').innerHTML = t.sec1NoatpText;"
    )

    with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Updated reporte_diputacion_agro_2.html successfully.")
    return True

if __name__ == '__main__':
    update_block_1_noatp()
