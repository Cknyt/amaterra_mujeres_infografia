# update_section4_comarcas.py
import re

new_sec4_html = """    <!-- BLOQUE 4: COMARCAS -->
    <section class="block-section" id="bloque-comarcas">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-tag" id="txt-sec4-tag">INDICADOR ESTRUCTURAL 4</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
              <line x1="8" y1="2" x2="8" y2="18"></line>
              <line x1="16" y1="6" x2="16" y2="22"></line>
            </svg>
            <span id="txt-sec4-title">Distribución Territorial por Comarcas (ADR)</span>
          </h2>
          <p class="section-desc" id="txt-sec4-desc">
            Análisis del <strong>% del total de mujeres por comarca</strong> en las 6 comarcas agrarias de Bizkaia. Revela una divergencia geográfica radical en la localización del talento profesional frente a las explotaciones comerciales no ATP.
          </p>
        </div>
        <div class="section-badge-group">
          <span class="badge badge-atp" id="badge-atp-pill-4">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp" id="badge-noatp-pill-4">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <!-- Micro-KPIs Resumen Territorial -->
      <div class="micro-kpi-grid">
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">41,05%</span>
          <span class="micro-kpi-lbl">Enkarterrialde ATP · Bastión profesional (78 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val noatp-text">26,00%</span>
          <span class="micro-kpi-lbl">Jata Ondo NO ATP · Mayor polo comercial (261 titulares)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">43% vs 26%</span>
          <span class="micro-kpi-lbl">Cuota Fem. ATP · Urremendi (43%) vs Jata Ondo (26%)</span>
        </div>
        <div class="micro-kpi-box">
          <span class="micro-kpi-val atp-text">44%</span>
          <span class="micro-kpi-lbl">Madurez 41-65 años · Enkarterrialde lidera relevo</span>
        </div>
      </div>

      <!-- Comparative Comarca Chart -->
      <div class="card" style="margin-bottom: 20px;">
        <div class="card-header">
          <div class="card-title">
            <span id="txt-sec4-chart-title">Distribución Comarcal Comparativa: % de Mujeres en cada Comarca</span>
          </div>
          <span class="badge badge-gray" id="txt-sec4-chart-badge">6 Comarcas de Bizkaia</span>
        </div>
        <div class="chart-box">
          <canvas id="chartComarcasComp"></canvas>
        </div>
      </div>

      <!-- Interactive Comarca Detail Cards -->
      <div class="comarca-cards-grid" id="comarca-interactive-grid"></div>

      <!-- DUAL COMMENTARY: ANÁLISIS COMARCAL ATP vs NO ATP -->
      <div class="dual-grid" style="margin-top: 24px;">
        <!-- COL ATP COMARCAS -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span>Distribución y Composición Territorial</span>
            </div>
            <span class="card-subtext">Base: 190 Mujeres ATP</span>
          </div>

          <div class="atp-subsector-narrative" style="display: flex; flex-direction: column; gap: 14px; margin-top: 10px;">
            <!-- Celda K46 -->
            <div class="insight-pill-card pill-emerald">
              <div class="pill-header">
                <span class="pill-tag tag-emerald">Distribución Territorial</span>
                <h4 class="pill-title">Concentración en Enkarterrialde y Contraste con Jata Ondo</h4>
              </div>
              <div class="pill-body">
                <p>La distribución territorial muestra diferencias entre mujeres y hombres ATP. <strong>Enkarterrialde concentra la mayor proporción de mujeres ATP, con un 41%</strong>, frente al 32% de los hombres. También se observa una mayor presencia relativa de mujeres en <strong>Urremendi</strong>, donde se concentra el 11% de las mujeres frente al 8% de los hombres.</p>
                <p>En <strong>Jata Ondo</strong>, en cambio, el peso relativo de los hombres es mayor: representa el 26% del total de hombres ATP, frente al 16% de las mujeres. En Urkiola también se observa una diferencia a favor de los hombres (12% frente a 10%). En Gorbeialde y Lea-Artibai, la distribución es idéntica entre ambos géneros: 15% y 7%, respectivamente.</p>
                <p>En conjunto, las mujeres ATP presentan una mayor concentración territorial en Enkarterrialde y Urremendi, mientras que los hombres tienen un peso relativo mayor en Jata Ondo y Urkiola.</p>
                <div class="pill-summary-box summary-emerald">
                  <strong>Para la infografía:</strong> El <strong>41% de las mujeres ATP se concentra en Enkarterrialde</strong>, frente al 32% de los hombres. Y como contraste: <strong>Jata Ondo concentra el 26% de los hombres ATP</strong>, frente al 16% de las mujeres.
                </div>
              </div>
            </div>

            <!-- Celda S44 -->
            <div class="insight-pill-card pill-emerald" style="border-top: 3px solid #059669;">
              <div class="pill-header">
                <span class="pill-tag tag-emerald">Composición por Género</span>
                <h4 class="pill-title">Variación de la Representatividad Femenina por Comarca</h4>
              </div>
              <div class="pill-body">
                <p>La composición por género muestra que los hombres son mayoría en todas las comarcas, aunque el peso relativo de mujeres y hombres presenta diferencias territoriales.</p>
                <p><strong>Urremendi y Enkarterrialde son las comarcas con mayor presencia relativa de mujeres, con un 43% y un 42%</strong>, respectivamente. En Gorbeialde, las mujeres representan el 36%, mientras que en Lea-Artibai alcanzan el 34%.</p>
                <p>Por debajo de la media del conjunto (36% de mujeres), se encuentran <strong>Urkiola (31%) y Jata Ondo (26%)</strong>. Esta última presenta la mayor diferencia entre hombres y mujeres: 74% de hombres frente a 26% de mujeres.</p>
                <div class="pill-summary-box summary-emerald">
                  <strong>Para la infografía:</strong> Las mujeres representan el <strong>43% de las personas ATP en Urremendi y el 42% en Enkarterrialde</strong>. En fuerte contraste, en <strong>Jata Ondo las mujeres representan el 26%</strong> de las personas ATP, frente al 74% de hombres.
                </div>
              </div>
            </div>

            <!-- Celda AE29 -->
            <div class="insight-pill-card pill-emerald" style="border-top: 3px solid #047857;">
              <div class="pill-header">
                <span class="pill-tag tag-emerald">Distribución Territorial por Edad</span>
                <h4 class="pill-title">Liderazgo de Enkarterrialde en Madurez y Juventud</h4>
              </div>
              <div class="pill-body">
                <p>La distribución territorial de las mujeres varía según el tramo de edad. Entre las <strong>mujeres de 18 a 40 años, Enkarterrialde concentra el mayor porcentaje (36%)</strong>, seguida de Gorbeialde y Lea-Artibai, ambas con un 6%, mientras que el resto de comarcas presentan porcentajes intermedios.</p>
                <p>En el grupo de <strong>41 a 65 años, Enkarterrialde vuelve a concentrar la mayor proporción de mujeres, con un 44%</strong>, muy por encima del resto de comarcas. Le siguen Gorbeialde (18%), Jata Ondo (14%) y, con porcentajes menores, Urkiola y Urremendi (9% cada una) y Lea-Artibai (7%).</p>
                <p>Entre las <strong>mujeres mayores de 65 años, cambia parcialmente el patrón: Jata Ondo concentra el mayor porcentaje (37%)</strong>, seguida de Enkarterrialde (26%) y Urremendi (16%). Gorbeialde y Lea-Artibai representan un 11% cada una, mientras que en Urkiola no se registran mujeres en este tramo (0%).</p>
                <div class="pill-summary-box summary-emerald">
                  <strong>Dato destacado para la infografía:</strong> Enkarterrialde concentra el <strong>44% de las mujeres de 41–65 años y el 36% de las mujeres de 18–40 años</strong>. Y en mayores de 65 años, <strong>Jata Ondo concentra el 37%</strong>, frente al 26% de Enkarterrialde.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COL NO ATP COMARCAS -->
        <div class="card card-noatp col-noatp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-noatp">NO ATP</span>
              <span>Distribución y Composición Territorial</span>
            </div>
            <span class="card-subtext">Base: 1.004 Mujeres No ATP Comerciales</span>
          </div>

          <div class="atp-subsector-narrative" style="display: flex; flex-direction: column; gap: 14px; margin-top: 10px;">
            <!-- Celda I71 -->
            <div class="insight-pill-card pill-amber">
              <div class="pill-header">
                <span class="pill-tag tag-amber">Distribución Territorial NO ATP</span>
                <h4 class="pill-title">Jata Ondo y Enkarterrialde Concentran la Mitad del Colectivo</h4>
              </div>
              <div class="pill-body">
                <p>La distribución territorial es bastante similar entre hombres y mujeres NO ATP. <strong>Jata Ondo concentra el mayor peso en ambos casos, con un 25% de los hombres y 26% de las mujeres</strong>, seguida de <strong>Enkarterrialde, con un 25% de los hombres y un 21% de las mujeres</strong>.</p>
                <p>En <strong>Urremendi y Lea-Artibai</strong>, las mujeres tienen un peso relativo ligeramente mayor que los hombres: 15% frente a 12% y 13% frente a 10%, respectivamente. En el resto de comarcas, los porcentajes son muy similares.</p>
                <div class="pill-summary-box summary-amber">
                  <strong>Dato clave para la infografía:</strong> <strong>Jata Ondo concentra el 26% de las mujeres NO ATP</strong> (261 mujeres), el porcentaje más alto entre todas las comarcas de Bizkaia.
                </div>
              </div>
            </div>

            <!-- Celda P71 -->
            <div class="insight-pill-card pill-amber" style="border-top: 3px solid #D97706;">
              <div class="pill-header">
                <span class="pill-tag tag-amber">Composición por Género según Comarca</span>
                <h4 class="pill-title">Máxima Representatividad en Lea-Artibai y Urremendi</h4>
              </div>
              <div class="pill-body">
                <p>En todas las comarcas, los hombres tienen un peso mayor que las mujeres en el colectivo no profesional comercial.</p>
                <p><strong>Lea-Artibai y Urremendi presentan la mayor proporción relativa de mujeres, con un 41% y 40%</strong>, respectivamente.</p>
                <p>En el extremo contrario, <strong>Enkarterrialde (32%) y Jata Ondo (37%)</strong> presentan una menor proporción de mujeres.</p>
                <div class="pill-summary-box summary-amber">
                  <strong>Conclusión Territorial NO ATP:</strong> En el modelo comercial a tiempo parcial, la costa oriental (Lea-Artibai y Urremendi) alcanza los mayores índices de paridad femenina (40%-41%), mientras que las zonas con vocación extensiva como Enkarterrialde ven descender la cuota femenina no ATP hasta el 32%.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="insight-card" style="margin-top: 20px;">
        <div class="insight-header">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
          <span id="txt-sec4-insight-title">Conclusión Analítica: La Polaridad Geográfica</span>
        </div>
        <p class="insight-text" id="txt-sec4-insight-text">
          Existe una inversión territorial asombrosa: <strong>Enkarterrialde</strong> es el bastión indiscutible del modelo profesional femenino, aglutinando por sí sola el <strong>41,05% de todas las mujeres ATP de Bizkaia</strong> (78 mujeres), debido a su relieve y vocación ganadera extensiva. En cambio, en el colectivo No ATP comercial, la mayor concentración se traslada a <strong>Jata Ondo</strong> con el <strong>26,00%</strong> (261 mujeres), impulsada por la huerta de ribera y la proximidad metropolitana.
        </p>
      </div>
    </section>
"""

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '    <!-- BLOQUE 4: COMARCAS -->'
start_line_idx = html.find(start_marker)

end_marker = '    <!-- BLOQUE 6: EDAD Y RELEVO -->'
end_line_idx = html.find(end_marker)

assert start_line_idx != -1 and end_line_idx != -1, f"Indices: {start_line_idx}, {end_line_idx}"

updated_html = html[:start_line_idx] + new_sec4_html + '\n' + html[end_line_idx:]

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Bloque 4 successfully updated!")
