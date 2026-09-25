# -*- coding: utf-8 -*-
"""
Script to generate reporte_diputacion_agro_2.html based on reporte_diputacion_agro.html
and the updated data/commentaries in 20260925_DatosExplotaciones.xlsx
"""
import json
import re
import sys

def build():
    with open('reporte_diputacion_agro.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Load extracted text from commentary_cells.json
    with open('scratch/commentary_cells.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)

    no_atp_c = comments['No_ATP']
    atp_c = comments['ATP']

    print("Loaded all comments successfully.")

    # 1. Update Title and Headers
    html = html.replace(
        '<title>Situación de las Mujeres en el Sector Agrario de Bizkaia | Emakumeen Egoera Bizkaiko Nekazaritza Sektorean</title>',
        '<title>Situación de las Mujeres en el Sector Agrario de Bizkaia (Reporte II) | Emakumeen Egoera Bizkaiko Nekazaritza Sektorean</title>'
    )

    # 2. Add extra CSS for literal commentary blocks and infografia callouts, and hide eco in NO ATP mode
    extra_css = """
    /* --- ESTILOS PARA COMENTARIOS TEXTUALES E INFOGRAFÍA (VERSIÓN 2) --- */
    .infografia-callout {
      margin-top: 14px;
      padding: 14px 16px;
      border-radius: 12px;
      font-size: 13px;
      line-height: 1.55;
      position: relative;
    }
    .infografia-callout.callout-atp {
      background: #ECFDF5;
      border: 1px solid #A7F3D0;
      color: #065F46;
    }
    .infografia-callout.callout-noatp {
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      color: #92400E;
    }
    .infografia-callout.callout-neutral {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      color: #1E293B;
    }
    .infografia-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      padding: 3px 8px;
      border-radius: 6px;
      margin-bottom: 8px;
    }
    .callout-atp .infografia-badge {
      background: #047857;
      color: #FFFFFF;
    }
    .callout-noatp .infografia-badge {
      background: #D97706;
      color: #FFFFFF;
    }
    .callout-neutral .infografia-badge {
      background: #334155;
      color: #FFFFFF;
    }
    .literal-text {
      font-size: 13.5px;
      line-height: 1.6;
      color: var(--slate-700);
      margin-bottom: 12px;
    }
    .literal-text p {
      margin-bottom: 10px;
    }
    .literal-text p:last-child {
      margin-bottom: 0;
    }
    .literal-text strong {
      color: var(--slate-900);
    }
    .callout-atp strong {
      color: #064E3B;
    }
    .callout-noatp strong {
      color: #78350F;
    }

    /* Ocultar bloque ecológico cuando el usuario selecciona Solo NO ATP */
    body.mode-noatp-only #bloque-ecologico {
      display: none !important;
    }
    """
    html = html.replace('</style>', extra_css + '\n  </style>')

    # 3. Update Hero KPI 3 with Cell I5
    # Cell I5: "El 16% de las personas productoras con fines de mercado son ATP en Bizkaia. Las mujeres representan el 36% de las personas ATP, frente al 64% de los hombres."
    txt_i5 = atp_c['I5'].strip()
    html = html.replace(
        '<div class="hero-stat-desc" id="txt-kpi3-desc">35,9% de los 529 ATPs de Bizkaia</div>',
        f'<div class="hero-stat-desc" id="txt-kpi3-desc" style="line-height: 1.4; margin-top: 4px;"><strong>Dato clave (ATP I5):</strong> {txt_i5}</div>'
    )

    # 4. Update Navigation: remove Forma Jurídica and renumber Edad to 5
    old_nav = """      <div class="nav-shortcuts">
        <a href="#bloque-subsectores" class="nav-chip" id="nav-chip-1">1. Subsectores</a>
        <a href="#bloque-superficie" class="nav-chip" id="nav-chip-2">2. Superficie</a>
        <a href="#bloque-ecologico" class="nav-chip" id="nav-chip-3">3. Ecológico</a>
        <a href="#bloque-comarcas" class="nav-chip" id="nav-chip-4">4. Comarcas</a>
        <a href="#bloque-juridica" class="nav-chip" id="nav-chip-5">5. Forma Jurídica</a>
        <a href="#bloque-edad" class="nav-chip" id="nav-chip-6">6. Edad y Relevo</a>
      </div>"""

    new_nav = """      <div class="nav-shortcuts">
        <a href="#bloque-subsectores" class="nav-chip" id="nav-chip-1">1. Subsectores</a>
        <a href="#bloque-superficie" class="nav-chip" id="nav-chip-2">2. Superficie</a>
        <a href="#bloque-ecologico" class="nav-chip" id="nav-chip-3">3. Ecológico (Solo ATP)</a>
        <a href="#bloque-comarcas" class="nav-chip" id="nav-chip-4">4. Comarcas</a>
        <a href="#bloque-edad" class="nav-chip" id="nav-chip-5">5. Edad y Relevo</a>
      </div>"""
    html = html.replace(old_nav, new_nav)

    # 5. Update Footer links (remove Forma Jurídica)
    old_footer_links = """      <div class="footer-links">
        <a href="#bloque-subsectores" id="txt-footer-link-1">Subsectores</a>
        <a href="#bloque-superficie" id="txt-footer-link-2">Superficie</a>
        <a href="#bloque-ecologico" id="txt-footer-link-3">Ecológico</a>
        <a href="#bloque-comarcas" id="txt-footer-link-4">Comarcas</a>
        <a href="#bloque-juridica" id="txt-footer-link-5">Forma Jurídica</a>
      </div>"""

    new_footer_links = """      <div class="footer-links">
        <a href="#bloque-subsectores" id="txt-footer-link-1">Subsectores</a>
        <a href="#bloque-superficie" id="txt-footer-link-2">Superficie</a>
        <a href="#bloque-ecologico" id="txt-footer-link-3">Ecológico (ATP)</a>
        <a href="#bloque-comarcas" id="txt-footer-link-4">Comarcas</a>
        <a href="#bloque-edad" id="txt-footer-link-5">Edad y Relevo</a>
      </div>"""
    html = html.replace(old_footer_links, new_footer_links)

    # 6. Helper function to format text with paragraphs
    def text_to_html_p(txt):
        paras = [p.strip() for p in txt.strip().split('\n\n') if p.strip()]
        out = []
        for p in paras:
            lines = p.split('\n')
            p_formatted = '<br>'.join(lines)
            out.append(f'<p>{p_formatted}</p>')
        return '\n'.join(out)

    # 7. SECTION 1: SUBSECTORES
    # Cell K15 in ATP card:
    # Cell S11 in ATP card as complementary callout
    # Cell J32 in NO ATP card
    k15_html = text_to_html_p(atp_c['K15'])
    s11_html = text_to_html_p(atp_c['S11'])
    j32_html = text_to_html_p(no_atp_c['J32'])

    # Old ATP text in sec1:
    old_sec1_atp_p = """          <p style="font-size: 13px; color: var(--slate-600); margin-bottom: 12px;" id="txt-sec1-atp-text">
            En el sector ATP destaca además una fuerte presencia en <strong>bovinos de leche (13,2%)</strong> y <strong>hortalizas de invernadero (8,9%)</strong>, sectores de alta exigencia laboral e inversión tecnológica.
          </p>"""

    new_sec1_atp_p = f"""          <div class="literal-text" id="txt-sec1-atp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--atp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial ATP (Celda K15):</div>
            {k15_html}
          </div>

          <div class="infografia-callout callout-atp" style="margin-bottom: 16px;">
            <div class="infografia-badge">Análisis por Género y Paridad (Celda S11)</div>
            <div class="literal-text" style="color: #065F46;">
              {s11_html}
            </div>
          </div>"""
    html = html.replace(old_sec1_atp_p, new_sec1_atp_p)

    # Old NO ATP text in sec1:
    old_sec1_noatp_p = """          <p style="font-size: 13px; color: var(--slate-600); margin-bottom: 12px;" id="txt-sec1-noatp-text">
            En el colectivo No ATP, el segundo y tercer puesto corresponden al <strong>ovino tradicional (12,2%)</strong> y a explotaciones <strong>no clasificadas (10,4%)</strong>, mientras que el bovino de leche apenas alcanza el 1%.
          </p>"""

    new_sec1_noatp_p = f"""          <div class="literal-text" id="txt-sec1-noatp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--noatp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial NO ATP (Celda J32):</div>
            {j32_html}
          </div>"""
    html = html.replace(old_sec1_noatp_p, new_sec1_noatp_p)

    # 8. SECTION 2: SUPERFICIE
    # Cell L34 in ATP card
    # Cell J56 in NO ATP card
    l34_html = text_to_html_p(atp_c['L34'])
    j56_html = text_to_html_p(no_atp_c['J56'])

    old_sec2_atp_p = """          <p style="font-size: 13px; color: var(--slate-600); margin-bottom: 14px;" id="txt-sec2-atp-text">
            Estructura equilibrada: el <strong>40,5%</strong> de las mujeres profesionales gestiona fincas medianas o grandes (>20 ha), con un 14,2% en explotaciones de más de 50 hectáreas.
          </p>"""

    new_sec2_atp_p = f"""          <div class="literal-text" id="txt-sec2-atp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--atp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial ATP (Celda L34):</div>
            {l34_html}
          </div>"""
    html = html.replace(old_sec2_atp_p, new_sec2_atp_p)

    old_sec2_noatp_p = """          <p style="font-size: 13px; color: var(--slate-600); margin-bottom: 14px;" id="txt-sec2-noatp-text">
            Extrema fragmentación: <strong>3 de cada 4 mujeres</strong> no alcanzan las 5 hectáreas, y solo un <strong>0,6%</strong> (6 mujeres en todo Bizkaia) tiene más de 50 ha.
          </p>"""

    new_sec2_noatp_p = f"""          <div class="literal-text" id="txt-sec2-noatp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--noatp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial NO ATP (Celda J56):</div>
            {j56_html}
          </div>"""
    html = html.replace(old_sec2_noatp_p, new_sec2_noatp_p)

    # 9. SECTION 3: ECOLÓGICO (REMOVE NO ATP completely, focus on ATP & N39)
    # Cell N39 in ATP
    n39_html = text_to_html_p(atp_c['N39'])

    # Find the entire bloque-ecologico section
    sec3_match = re.search(r'(<section class="block-section" id="bloque-ecologico">.*?</section>)', html, re.DOTALL)
    if sec3_match:
        old_sec3 = sec3_match.group(1)

        new_sec3 = f"""    <!-- BLOQUE 3: ECOLÓGICO (EXCLUSIVO ATP) -->
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

      <!-- Highlight Banner ATP -->
      <div class="hero-card" style="background: linear-gradient(135deg, #064E3B 0%, #047857 100%); padding: 22px 28px; margin-bottom: 24px;">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px;">
          <div style="max-width: 820px;">
            <div style="font-size: 11.5px; font-weight: 800; color: #6EE7B7; text-transform: uppercase; letter-spacing: 0.8px;" id="txt-sec3-banner-tag">SOSTENIBILIDAD Y TRANSICIÓN ECOLÓGICA ATP</div>
            <div style="font-size: 21px; font-weight: 800; color: #FFFFFF; margin-top: 4px;" id="txt-sec3-banner-title">
              Liderazgo de las Mujeres Profesionales ATP en Producción Ecológica
            </div>
            <div style="font-size: 13.5px; color: rgba(255,255,255,0.9); margin-top: 6px; line-height: 1.5;" id="txt-sec3-banner-desc">
              El <strong>12% de las mujeres ATP produce en ecológico</strong> (frente al 9% de los hombres). Además, representan el <strong>41% de todas las personas ATP con producción ecológica</strong> de Bizkaia.
            </div>
          </div>
          <div style="background: rgba(255,255,255,0.15); padding: 14px 24px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
            <div style="font-size: 11px; text-transform: uppercase; color: #A7F3D0; font-weight: 700;" id="txt-sec3-banner-kpi-lbl">Tasa Eco Femenina ATP</div>
            <div style="font-size: 32px; font-weight: 800; color: #FFFFFF;">11,58%</div>
            <div style="font-size: 11px; color: #A7F3D0; font-weight: 600;">22 de 190 Mujeres ATP</div>
          </div>
        </div>
      </div>

      <!-- Grid con tarjeta de datos y tarjeta de análisis literal de Celda N39 -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 20px;">
        <!-- Card 1: Desglose cuantitativo ATP -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span id="txt-sec3-atp-card-title">Certificaciones y Grado de Conversión Ecológica</span>
            </div>
            <span class="card-subtext" id="txt-sec3-atp-base">Base: 190 Mujeres ATP</span>
          </div>
          <div class="metric-hero">
            <span class="metric-val atp-text">11,58%</span>
            <span class="metric-unit" id="txt-sec3-atp-unit">con actividad ecológica (22 mujeres)</span>
          </div>
          <p style="font-size: 13px; color: var(--slate-600); margin-bottom: 14px;" id="txt-sec3-atp-text">
            De las 22 mujeres ecológicas ATP: <strong>17 disponen de certificado oficial</strong> (8,95%), 4 certifican una parte (2,11%) y 1 está en proceso (0,53%).
          </p>

          <div class="segment-list" id="list-ecologico-atp"></div>

          <div style="margin-top: 16px; padding: 12px; background: var(--atp-light); border-radius: 10px; border: 1px solid var(--atp-border); font-size: 12px; color: var(--atp-text);" id="txt-sec3-atp-note">
            <strong>Liderazgo femenino en el sector eco ATP:</strong> Las 22 mujeres representan el <strong>40,7% de todas las explotaciones ecológicas profesionales</strong> de Bizkaia (54 en total: 32 hombres y 22 mujeres).
          </div>
        </div>

        <!-- Card 2: Análisis textual literal de Celda N39 -->
        <div class="card card-atp col-atp" style="border-top: 4px solid var(--atp-primary);">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">COMENTARIO OFICIAL</span>
              <span>Análisis Textual (Celda N39 de Hoja ATP)</span>
            </div>
            <span class="card-subtext">Datos oficiales Diputación</span>
          </div>

          <div class="literal-text" style="margin-top: 8px;">
            {n39_html}
          </div>

          <div class="infografia-callout callout-atp" style="margin-top: 18px;">
            <div class="infografia-badge">Para la infografía · Clave Ecológica</div>
            <div style="font-size: 13.5px; font-weight: 700; color: #064E3B; margin-bottom: 4px;">
              Mayor vocación ecológica entre las mujeres:
            </div>
            <p style="font-size: 13px; color: #065F46; line-height: 1.5; margin: 0;">
              El <strong>12% de las mujeres ATP produce en ecológico frente al 9% de los hombres</strong>. Además, la presencia femenina en el total ecológico profesional (41%) supera notablemente su representatividad en el censo general ATP (36%).
            </p>
          </div>
        </div>
      </div>
    </section>"""
        html = html.replace(old_sec3, new_sec3)
        print("Replaced bloque-ecologico successfully.")

    # 10. SECTION 4: COMARCAS
    # Insert literal commentaries of K46, S44, AE29 for ATP
    # and I71, P71 for NO ATP
    k46_html = text_to_html_p(atp_c['K46'])
    s44_html = text_to_html_p(atp_c['S44'])
    ae29_html = text_to_html_p(atp_c['AE29'])
    i71_html = text_to_html_p(no_atp_c['I71'])
    p71_html = text_to_html_p(no_atp_c['P71'])

    comarcas_dual_commentary = f"""
      <!-- DUAL COMMENTARY: ANÁLISIS COMARCAL ATP (K46, S44, AE29) vs NO ATP (I71, P71) -->
      <div class="dual-grid" style="margin-top: 24px;">
        <!-- COL ATP COMARCAS -->
        <div class="card card-atp col-atp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-atp">ATP</span>
              <span>Análisis Territorial ATP (Celdas K46, S44 y AE29)</span>
            </div>
            <span class="card-subtext">Base: 190 Mujeres ATP</span>
          </div>

          <!-- Celda K46 -->
          <div class="literal-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--atp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Distribución Territorial (Celda K46):</div>
            {k46_html}
          </div>

          <!-- Celda S44 -->
          <div class="infografia-callout callout-atp" style="margin-top: 14px;">
            <div class="infografia-badge">Composición por Género (Celda S44)</div>
            <div class="literal-text" style="color: #065F46;">
              {s44_html}
            </div>
          </div>

          <!-- Celda AE29 -->
          <div class="infografia-callout callout-atp" style="margin-top: 14px;">
            <div class="infografia-badge">Distribución Territorial por Edad (Celda AE29)</div>
            <div class="literal-text" style="color: #065F46;">
              {ae29_html}
            </div>
          </div>
        </div>

        <!-- COL NO ATP COMARCAS -->
        <div class="card card-noatp col-noatp">
          <div class="card-header">
            <div class="card-title">
              <span class="badge badge-noatp">NO ATP</span>
              <span>Análisis Territorial NO ATP (Celdas I71 y P71)</span>
            </div>
            <span class="card-subtext">Base: 1.004 Mujeres No ATP</span>
          </div>

          <!-- Celda I71 -->
          <div class="literal-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--noatp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Distribución Territorial NO ATP (Celda I71):</div>
            {i71_html}
          </div>

          <!-- Celda P71 -->
          <div class="infografia-callout callout-noatp" style="margin-top: 14px;">
            <div class="infografia-badge">Composición por Género según Comarca (Celda P71)</div>
            <div class="literal-text" style="color: #92400E;">
              {p71_html}
            </div>
          </div>
        </div>
      </div>
"""
    # Insert comarcas_dual_commentary right before the existing insight-card in bloque-comarcas
    old_comarcas_insight = '<div class="insight-card" style="margin-top: 20px;">'
    html = html.replace(old_comarcas_insight, comarcas_dual_commentary + '\n      ' + old_comarcas_insight)
    print("Added Comarcas dual commentaries successfully.")

    # 11. SECTION 5: CONDICIÓN JURÍDICA (REMOVE COMPLETELY!)
    juridica_pattern = r'(<!-- BLOQUE 5: FORMA JURÍDICA -->\s*<section class="block-section" id="bloque-juridica">.*?</section>)'
    if re.search(juridica_pattern, html, re.DOTALL):
        html = re.sub(juridica_pattern, '', html, flags=re.DOTALL)
        print("Removed bloque-juridica completely.")
    else:
        print("WARNING: bloque-juridica pattern not found, trying fallback removal")
        sec_jur_fallback = re.search(r'(<section class="block-section" id="bloque-juridica">.*?</section>)', html, re.DOTALL)
        if sec_jur_fallback:
            html = html.replace(sec_jur_fallback.group(1), '')
            print("Removed bloque-juridica via fallback.")

    # 12. SECTION 6 (NOW 5): EDAD Y RELEVO
    # Renumber tag: INDICADOR ESTRUCTURAL 6 -> INDICADOR ESTRUCTURAL 5
    html = html.replace(
        '<div class="section-tag" id="txt-sec6-tag">INDICADOR ESTRUCTURAL 6</div>',
        '<div class="section-tag" id="txt-sec6-tag">INDICADOR ESTRUCTURAL 5</div>'
    )

    # Insert literal texts:
    # Cell P37 in ATP card
    # Cell I20 in NO ATP card
    p37_html = text_to_html_p(atp_c['P37'])
    i20_html = text_to_html_p(no_atp_c['I20'])

    # Old ATP card in bloque-edad:
    old_edad_atp_content = """          <div class="metric-hero">
            <span class="metric-val atp-text">53 años</span>
            <span class="metric-unit" id="txt-sec6-atp-unit">edad media (frente a 66 en No ATP)</span>
          </div>
          <div class="segment-list" id="list-edad-atp"></div>"""

    new_edad_atp_content = f"""          <div class="metric-hero">
            <span class="metric-val atp-text">53 años</span>
            <span class="metric-unit" id="txt-sec6-atp-unit">edad media (frente a 66 en No ATP)</span>
          </div>

          <div class="literal-text" id="txt-sec6-atp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--atp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial ATP (Celda P37):</div>
            {p37_html}
          </div>

          <div class="segment-list" id="list-edad-atp"></div>"""
    html = html.replace(old_edad_atp_content, new_edad_atp_content)

    # Old NO ATP card in bloque-edad:
    old_edad_noatp_content = """          <div class="metric-hero">
            <span class="metric-val noatp-text">66 años</span>
            <span class="metric-unit" id="txt-sec6-noatp-unit">edad media (riesgo de cese)</span>
          </div>
          <div class="segment-list" id="list-edad-noatp"></div>"""

    new_edad_noatp_content = f"""          <div class="metric-hero">
            <span class="metric-val noatp-text">66 años</span>
            <span class="metric-unit" id="txt-sec6-noatp-unit">edad media (riesgo de cese)</span>
          </div>

          <div class="literal-text" id="txt-sec6-noatp-text">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--noatp-dark); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Comentario Oficial NO ATP (Celda I20):</div>
            {i20_html}
          </div>

          <div class="segment-list" id="list-edad-noatp"></div>"""
    html = html.replace(old_edad_noatp_content, new_edad_noatp_content)

    # 13. JS & I18N ADJUSTMENTS
    # Update I18N.es and I18N.eu to prevent looking for missing elements (e.g. sec5 elements)
    # In setLang function: wrap sec5 element lookups in safe checks `if (document.getElementById(...))`
    # and update renderEcologico to not look for noatpList
    html = html.replace(
        "document.getElementById('nav-chip-5').textContent = t.navChip5;\n      document.getElementById('nav-chip-6').textContent = t.navChip6;",
        "if (document.getElementById('nav-chip-5')) document.getElementById('nav-chip-5').textContent = t.navChip6;"
    )

    # Safe element updates in setLang for sec5:
    sec5_js_pattern = r"(// Bloque 5\s+document\.getElementById\('txt-sec5-tag'\).*?// Bloque 6)"
    safe_sec5_js = """// Bloque 5 (Condición jurídica eliminada)
      // Bloque 6"""
    html = re.sub(sec5_js_pattern, safe_sec5_js, html, flags=re.DOTALL)

    # Remove renderFormaJuridica call from setLang and DOMContentLoaded
    html = html.replace("renderFormaJuridica();", "// renderFormaJuridica();")

    # In renderEcologico: remove noatpList rendering so it doesn't fail
    old_render_eco = """    function renderEcologico() {
      const atpList = document.getElementById('list-ecologico-atp');
      const noatpList = document.getElementById('list-ecologico-noatp');
      const t = I18N[CURRENT_LANG] || I18N.es;
      const mLabel = CURRENT_LANG === 'eu' ? 'em.' : 'm.';

      atpList.innerHTML = '';
      noatpList.innerHTML = '';

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

      DATA_EXCEL.No_ATP.ecologico.forEach(e => {
        noatpList.innerHTML += `
          <div class="segment-item">
            <div class="segment-item-top">
              <span class="segment-item-name">${translateName(e.tipo)}</span>
              <span class="segment-item-pct noatp-pct">${e.pct_m_de_1004}% <span style="font-size:11px;font-weight:500;color:var(--slate-500);">(${e.m} ${mLabel})</span></span>
            </div>
            <div class="segment-item-sub">${t.hombresPrefix}: ${e.h} | ${t.mujeresPrefix}: ${e.m}</div>
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-noatp" style="width: ${e.pct_m_de_1004 * 8}%;"></div></div>
          </div>
        `;
      });
    }"""

    new_render_eco = """    function renderEcologico() {
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
    html = html.replace(old_render_eco, new_render_eco)

    # In setLang, make sure noatp eco elements don't cause TypeError if absent
    html = html.replace(
        "document.getElementById('txt-sec3-noatp-card-title').textContent = t.sec3NoatpCardTitle;\n      document.getElementById('txt-sec3-noatp-base').textContent = t.sec3NoatpBase;\n      document.getElementById('txt-sec3-noatp-unit').textContent = t.sec3NoatpUnit;\n      document.getElementById('txt-sec3-noatp-text').innerHTML = t.sec3NoatpText;\n      document.getElementById('txt-sec3-noatp-note').innerHTML = t.sec3NoatpNote;",
        "if (document.getElementById('txt-sec3-noatp-card-title')) {\n        document.getElementById('txt-sec3-noatp-card-title').textContent = t.sec3NoatpCardTitle;\n        document.getElementById('txt-sec3-noatp-base').textContent = t.sec3NoatpBase;\n        document.getElementById('txt-sec3-noatp-unit').textContent = t.sec3NoatpUnit;\n        document.getElementById('txt-sec3-noatp-text').innerHTML = t.sec3NoatpText;\n        document.getElementById('txt-sec3-noatp-note').innerHTML = t.sec3NoatpNote;\n      }"
    )

    # Update Footer link 5 in setLang
    html = html.replace(
        "document.getElementById('txt-footer-link-5').textContent = t.navChip5.replace(/^\\d+\\.\\s*/, '');",
        "if (document.getElementById('txt-footer-link-5')) document.getElementById('txt-footer-link-5').textContent = t.navChip6.replace(/^\\d+\\.\\s*/, '');"
    )

    # Save to reporte_diputacion_agro_2.html
    with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as out:
        out.write(html)

    print("reporte_diputacion_agro_2.html generated successfully! Length:", len(html))

if __name__ == '__main__':
    build()
