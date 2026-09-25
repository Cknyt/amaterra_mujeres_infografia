# -*- coding: utf-8 -*-
"""
Update Block 1 (ATP Subsectores) in reporte_diputacion_agro_2.html to improve legibility:
- Eliminates technical labels like 'Comentario Oficial ATP (Celda K15)' and 'Análisis por Género y Paridad (Celda S11)'.
- Implements an editorial bipartite structure (Left: Data/Ranking/Table, Right: Structured Insights with micro-badges and conclusions).
- Adds top micro-KPI summary row (57% Vacuno, 8.9% Invernadero, 71% Caprino, 50% Paridad).
- Keeps bilingual and responsive compatibility.
"""
import re

def update_block_1():
    with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add CSS styles
    new_css = """
    /* --- SUBSECTORES ATP: SPLIT LAYOUT Y PÍLDORAS ESTRUCTURADAS --- */
    .atp-subsector-split {
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
      margin-top: 14px;
    }
    @media (min-width: 1100px) {
      body.mode-atp-only .atp-subsector-split {
        grid-template-columns: 1.02fr 1.18fr;
        gap: 28px;
        align-items: start;
      }
    }
    .subsector-side-title {
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--slate-500);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .subsector-side-title svg {
      color: var(--atp-primary);
    }
    .micro-kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }
    .micro-kpi-box {
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 10px;
      padding: 10px 12px;
      text-align: left;
    }
    .micro-kpi-box.kpi-emerald {
      background: #F4FBF7;
      border-color: #A7F3D0;
    }
    .micro-kpi-box.kpi-purple {
      background: #FAF5FF;
      border-color: #E9D5FF;
    }
    .micro-kpi-val {
      font-size: 19px;
      font-weight: 800;
      color: var(--slate-900);
      line-height: 1.1;
      display: block;
    }
    .micro-kpi-box.kpi-emerald .micro-kpi-val {
      color: #065F46;
    }
    .micro-kpi-box.kpi-purple .micro-kpi-val {
      color: #6B21A8;
    }
    .micro-kpi-lbl {
      font-size: 11px;
      color: var(--slate-600);
      font-weight: 600;
      margin-top: 3px;
      display: block;
      line-height: 1.25;
    }
    .insight-pill-card {
      border-radius: 14px;
      padding: 16px 18px;
      margin-bottom: 14px;
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
    }
    .insight-pill-card.pill-emerald {
      background: #F4FBF7;
      border-color: #A7F3D0;
    }
    .insight-pill-card.pill-purple {
      background: #FAF5FF;
      border-color: #E9D5FF;
    }
    .pill-header {
      margin-bottom: 10px;
    }
    .pill-tag {
      display: inline-block;
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.7px;
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }
    .pill-tag.tag-emerald {
      background: #047857;
      color: #FFFFFF;
    }
    .pill-tag.tag-purple {
      background: #7E22CE;
      color: #FFFFFF;
    }
    .pill-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 14.5px;
      font-weight: 800;
      color: var(--slate-900);
      line-height: 1.35;
    }
    .pill-body {
      font-size: 13px;
      line-height: 1.55;
      color: var(--slate-700);
    }
    .pill-body p {
      margin-bottom: 8px;
    }
    .pill-body p:last-child {
      margin-bottom: 0;
    }
    .pill-summary-box {
      margin-top: 12px;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 12.5px;
      line-height: 1.45;
    }
    .pill-summary-box.summary-emerald {
      background: rgba(4, 120, 87, 0.08);
      border-left: 3px solid #047857;
      color: #064E3B;
    }
    .pill-summary-box.summary-purple {
      background: rgba(126, 34, 206, 0.08);
      border-left: 3px solid #7E22CE;
      color: #581C87;
    }
    .paridad-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin: 10px 0;
    }
    .paridad-item {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 12.5px;
      line-height: 1.4;
      color: var(--slate-700);
      background: rgba(255, 255, 255, 0.7);
      padding: 7px 10px;
      border-radius: 8px;
      border: 1px solid rgba(233, 213, 255, 0.6);
    }
    .paridad-badge {
      flex-shrink: 0;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 6px;
      letter-spacing: 0.3px;
    }
    .paridad-badge.badge-green {
      background: #D1FAE5;
      color: #065F46;
    }
    .paridad-badge.badge-blue {
      background: #DBEAFE;
      color: #1E40AF;
    }
    .paridad-badge.badge-purple {
      background: #F3E8FF;
      color: #6B21A8;
    }
"""
    if '/* --- SUBSECTORES ATP: SPLIT LAYOUT' not in html:
        html = html.replace('</style>', new_css + '\n  </style>')

    # 2. Build the new ATP card for Section 1
    new_atp_card = """        <!-- COL ATP SUBSECTORES -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span id="txt-sec1-atp-card-title">Subsectores en Mujeres Profesionales</span>
            </div>
            <span class="card-subtext" id="txt-sec1-atp-base">Base: 190 Mujeres ATP (100%)</span>
          </div>

          <!-- Micro KPIs de síntesis sectorial -->
          <div class="micro-kpi-grid">
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">43,7%</span>
              <span class="micro-kpi-lbl">Bovino Carne (83 mujeres)</span>
            </div>
            <div class="micro-kpi-box kpi-emerald">
              <span class="micro-kpi-val">57,0%</span>
              <span class="micro-kpi-lbl">Vacuno Total (Carne + Leche)</span>
            </div>
            <div class="micro-kpi-box kpi-purple">
              <span class="micro-kpi-val">71,4%</span>
              <span class="micro-kpi-lbl">Caprino (Liderazgo Femenino)</span>
            </div>
            <div class="micro-kpi-box kpi-purple">
              <span class="micro-kpi-val">50% / 50%</span>
              <span class="micro-kpi-lbl">Porcino y Frutícola (Paridad)</span>
            </div>
          </div>

          <!-- Estructura Bipartita: Datos a la izquierda / Análisis cualitativo a la derecha -->
          <div class="atp-subsector-split">
            <!-- Zona Izquierda: Datos y Ranking Top 5 -->
            <div class="atp-subsector-data">
              <div class="subsector-side-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                Ranking de Actividad Femenina
              </div>

              <div class="segment-list" id="list-subsectores-atp"></div>

              <button class="btn-toggle-expand" onclick="toggleExpand('table-subsectores-atp', this)" style="margin-top: 14px;">
                <span id="txt-sec1-atp-btn">Mostrar tabla completa de 15 subsectores ATP</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </button>

              <div id="table-subsectores-atp" class="table-responsive" style="display: none; margin-top: 12px;">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th id="th-sub-atp-name">Subsector</th>
                      <th class="num" id="th-sub-atp-h">Hombres</th>
                      <th class="num" id="th-sub-atp-m">Mujeres</th>
                      <th class="num" id="th-sub-atp-pct">% Mujeres (de 190)</th>
                    </tr>
                  </thead>
                  <tbody id="tbody-subsectores-atp"></tbody>
                </table>
              </div>
            </div>

            <!-- Zona Derecha: Píldoras de Hallazgos y Análisis Narrativo -->
            <div class="atp-subsector-narrative" id="txt-sec1-atp-text">
              <!-- Píldora 1: Especialización en Vacuno -->
              <div class="insight-pill-card pill-emerald">
                <div class="pill-header">
                  <span class="pill-tag tag-emerald">Especialización Productiva</span>
                  <h4 class="pill-title">Concentración en Ganado Vacuno vs. Diversificación Masculina</h4>
                </div>
                <div class="pill-body">
                  <p>En comparación con los hombres, la actividad de las mujeres ATP se concentra en mayor medida en el ganado bovino. El <strong>57% de las mujeres ATP se dedica a explotaciones de vacuno</strong>, principalmente de carne (<strong>44%</strong>) y, en menor medida, de leche (<strong>13%</strong>). A continuación, se sitúan las hortalizas en invernadero (<strong>9%</strong>).</p>
                  <p>En el caso de los hombres ATP, aunque el vacuno también representa una parte importante de la actividad (47%), su distribución es algo más diversa: el <strong>33%</strong> se dedica al vacuno de carne, el <strong>14%</strong> al vacuno de leche y un <strong>19% a las hortalizas en invernadero</strong>.</p>
                  <div class="pill-summary-box summary-emerald">
                    <strong>Conclusión:</strong> Se muestra una mayor concentración de la actividad de las mujeres ATP en el sector bovino, mientras que entre los hombres existe una distribución algo más diversificada, con un peso relevante también de la horticultura en invernadero.
                  </div>
                </div>
              </div>

              <!-- Píldora 2: Paridad y Pequeños Animales -->
              <div class="insight-pill-card pill-purple">
                <div class="pill-header">
                  <span class="pill-tag tag-purple">Perspectiva de Género</span>
                  <h4 class="pill-title">Distribución por Género: Liderazgo en Pequeños Animales y Paridad</h4>
                </div>
                <div class="pill-body">
                  <p>Si revisamos los datos poniendo el foco en cómo se distribuyen los distintos subsectores según el género de las personas titulares, se observa que, en la mayoría de ellos, los hombres tienen una mayor presencia. Sin embargo, surgen claras excepciones de liderazgo femenino y equilibrio:</p>
                  
                  <div class="paridad-list">
                    <div class="paridad-item">
                      <span class="paridad-badge badge-green">71% Mujeres</span>
                      <div><strong>Explotaciones de caprinos:</strong> Principal excepción sectorial, donde las mujeres representan el 71% de los proyectos frente al 29% masculino.</div>
                    </div>
                    <div class="paridad-item">
                      <span class="paridad-badge badge-blue">50% / 50%</span>
                      <div><strong>Porcino y Fruticultura:</strong> Distribución en paridad equilibrada; hombres y mujeres representan exactamente el 50% de las titularidades en ambos casos.</div>
                    </div>
                    <div class="paridad-item">
                      <span class="paridad-badge badge-purple">48% Mujeres</span>
                      <div><strong>Aves ponedoras:</strong> Distribución prácticamente equilibrada, con un 48% de proyectos correspondientes a mujeres y un 52% a hombres.</div>
                    </div>
                  </div>

                  <div class="pill-summary-box summary-purple">
                    <strong>Conclusión infográfica:</strong> Los datos apuntan a una <strong>mayor presencia relativa de las mujeres en aquellos subsectores vinculados a pequeños animales</strong>.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>"""

    # Locate and replace old ATP card in Section 1
    pattern = r'(<!-- COL ATP SUBSECTORES -->\s*<div class="card card-atp col-atp">.*?</div>\s*</div>\s*</div>\s*)(<!-- COL NO ATP SUBSECTORES -->)'
    # Or match from COL ATP SUBSECTORES to COL NO ATP SUBSECTORES
    m = re.search(r'(<!-- COL ATP SUBSECTORES -->\s*<div class="card card-atp col-atp">.*?)(<!-- COL NO ATP SUBSECTORES -->)', html, re.DOTALL)
    if m:
        html = html[:m.start(1)] + new_atp_card + '\n\n        ' + html[m.start(2):]
        print("Replaced ATP subsector card successfully!")
    else:
        print("ERROR: Could not locate COL ATP SUBSECTORES!")
        return False

    with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Updated reporte_diputacion_agro_2.html successfully.")
    return True

if __name__ == '__main__':
    update_block_1()
