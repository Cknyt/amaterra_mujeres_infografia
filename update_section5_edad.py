# update_section5_edad.py
import re

new_sec5_html = """    <!-- BLOQUE 6: EDAD Y RELEVO -->
    <section class="block-section" id="bloque-edad">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-tag" id="txt-sec6-tag">INDICADOR ESTRUCTURAL 5</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span id="txt-sec6-title">Pirámide de Edad y Alerta de Relevo Generacional</span>
          </h2>
          <p class="section-desc" id="txt-sec6-desc">
            Comparativa de la <strong>edad media</strong> y la distribución de las mujeres en los tramos oficiales: 18-40 años, 41-65 años y mayores de 65 años.
          </p>
        </div>
        <div class="section-badge-group">
          <span class="badge badge-atp" id="badge-atp-pill-6">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp" id="badge-noatp-pill-6">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <!-- Micro-KPIs Resumen Edad y Relevo -->
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
      </div>

      <div class="dual-grid">
        <!-- COL ATP EDAD -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span id="txt-sec6-atp-card-title">Demografía Femenina Profesional</span>
            </div>
            <span class="card-subtext" id="txt-sec6-atp-base">Edad Media: 53 años (Base: 190 Mujeres ATP)</span>
          </div>

          <div class="atp-subsector-split">
            <!-- Datos Pirámide ATP -->
            <div class="atp-subsector-data">
              <div class="metric-hero">
                <span class="metric-val atp-text">53 años</span>
                <span class="metric-unit" id="txt-sec6-atp-unit">edad media (frente a 66 en No ATP)</span>
              </div>

              <div class="segment-list" id="list-edad-atp"></div>

              <div class="pill-summary-box summary-emerald" style="margin-top: 14px;">
                <strong>Pirámide Sostenible:</strong> El <strong>86,3% de las mujeres profesionales en activo son menores de 65 años</strong>, concentrando su núcleo en la etapa de máxima experiencia productiva y consolidación técnica.
              </div>
            </div>

            <!-- Narrativa Celda P37 -->
            <div class="atp-subsector-narrative" id="txt-sec6-atp-text">
              <div class="insight-pill-card pill-emerald">
                <div class="pill-header">
                  <span class="pill-tag tag-emerald">Estructura Demográfica ATP</span>
                  <h4 class="pill-title">Concentración en Madurez y Dinámica de Relevo</h4>
                </div>
                <div class="pill-body">
                  <p>La distribución por edad muestra una estructura similar entre hombres y mujeres ATP, con una clara <strong>concentración en el tramo de 41 a 65 años. Este grupo representa el 69% de los hombres ATP y el 73% de las mujeres</strong>.</p>
                  <p>En el grupo de <strong>18 a 40 años, los hombres tienen un mayor peso relativo, con un 24%, frente al 17% de las mujeres</strong>. Esta diferencia se invierte en el grupo de mayores de 65 años, donde las mujeres representan el <strong>10% y los hombres el 7%</strong>.</p>
                  <p>Se observa una mayor presencia relativa de hombres en el tramo más joven y de mujeres en el tramo de mayor edad.</p>
                  <div class="pill-summary-box summary-emerald">
                    <strong>Dato clave para la infografía:</strong> El <strong>73% de las mujeres ATP se concentra entre 41 y 65 años</strong>, formando el núcleo productivo del agro profesional en Bizkaia con un relevo generacional joven (17%) que triplica al colectivo no profesional.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COL NO ATP EDAD -->
        <div class="card card-noatp col-noatp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-noatp">NO ATP</span>
              <span id="txt-sec6-noatp-card-title">Demografía Femenina Comercial</span>
            </div>
            <span class="card-subtext" id="txt-sec6-noatp-base">Edad Media: 66 años (Base: 1.004 Mujeres No ATP)</span>
          </div>

          <div class="atp-subsector-split">
            <!-- Datos Pirámide NO ATP -->
            <div class="atp-subsector-data">
              <div class="metric-hero">
                <span class="metric-val noatp-text">66 años</span>
                <span class="metric-unit" id="txt-sec6-noatp-unit">edad media (riesgo de cese)</span>
              </div>

              <div class="segment-list" id="list-edad-noatp"></div>

              <div class="pill-summary-box summary-amber" style="margin-top: 14px; border-left: 3px solid #DC2626;">
                <strong style="color: #DC2626;">Alerta Demográfica:</strong> <strong>527 mujeres (52,5%) superan los 65 años</strong>. Más de la mitad de las explotaciones comerciales no profesionales afrontan riesgo inminente de cese en esta década por falta de relevo tutelado.
              </div>
            </div>

            <!-- Narrativa Celda I20 -->
            <div class="atp-subsector-narrative" id="txt-sec6-noatp-text">
              <div class="insight-pill-card pill-amber">
                <div class="pill-header">
                  <span class="pill-tag tag-amber">Distribución por Edad NO ATP</span>
                  <h4 class="pill-title">Estructura Envejecida y Déficit Juvenil</h4>
                </div>
                <div class="pill-body">
                  <p>La distribución por edad muestra una <strong>estructura más envejecida entre las mujeres no ATP que entre los hombres</strong>. En ambos casos, la mayor concentración se encuentra en el grupo de mayores de 65 años, pero este tramo representa el <strong>74% de las mujeres, frente al 60% de los hombres</strong>.</p>
                  <p>En el grupo de 41 a 65 años, los hombres tienen un mayor peso relativo, con un <strong>28%, frente al 20% de las mujeres</strong>. Esta diferencia también se observa entre las personas de 18 a 40 años, donde los hombres representan el <strong>12% y las mujeres el 6%</strong>.</p>
                  <p>Las mujeres no ATP con fines de mercado presentan una mayor concentración en las edades más avanzadas, casi tres de cada cuatro mujeres tienen más de 65 años, frente a seis de cada diez hombres. En cambio, los hombres tienen mayor peso relativo tanto en el tramo de 18–40 como en el de 41–65 años.</p>
                  <div class="pill-summary-box summary-amber">
                    <strong>Dato destacado para la infografía:</strong> El <strong>74% de las mujeres no ATP con fines de mercado tiene más de 65 años</strong>, frente al 60% de los hombres. Y el contraste es bastante claro: <strong>solo el 6% de las mujeres tiene entre 18 y 40 años</strong>, frente al 12% de los hombres.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="insight-card">
        <div class="insight-header" style="color: #DC2626;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <span id="txt-sec6-insight-title">Alerta Demográfica: Riesgo Inminente de Abandono</span>
        </div>
        <p class="insight-text" id="txt-sec6-insight-text">
          Existe un abismo generacional de <strong>13 años de diferencia en la edad media</strong> (53 años en ATP frente a 66 años en No ATP). En el colectivo No ATP, <strong>más de la mitad de las mujeres (52,5% - 527 titulares) superan la edad oficial de jubilación</strong>, mientras que las menores de 40 años apenas suponen el 5,2%. Sin un plan de relevo tutelado, más de 500 explotaciones corren riesgo de cese en la presente década.
        </p>
      </div>
    </section>
"""

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '    <!-- BLOQUE 6: EDAD Y RELEVO -->'
start_line_idx = html.find(start_marker)

end_marker = '  </main>'
end_line_idx = html.find(end_marker)

assert start_line_idx != -1 and end_line_idx != -1, f"Indices: {start_line_idx}, {end_line_idx}"

updated_html = html[:start_line_idx] + new_sec5_html + '\n  ' + html[end_line_idx:]

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Bloque 5 (Edad y Relevo) successfully updated!")
