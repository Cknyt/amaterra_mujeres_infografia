# -*- coding: utf-8 -*-
"""
Builder for explorador_agro_bizkaia.html
Full-spectrum interactive explorer from top-level census to microdata,
with dynamic gender-lens insight generator.
"""
import openpyxl
import json
import os

print("Processing Excel data for explorador_agro_bizkaia.html...")

excel_file = "20260924_0734_DATOS EXPLOTACIONES DE ALTA_ULTIMA VERSIÓN.xlsx"
wb = openpyxl.load_workbook(excel_file, read_only=True)
ws = wb['Hoja1']
rows = ws.iter_rows(values_only=True)
headers = next(rows)

adrs, munis, grps, jurs, otes = [], [], [], [], []

def get_id(val, lst):
    if val not in lst:
        lst.append(val)
    return lst.index(val)

records = []
for idx, r in enumerate(rows, 1):
    sex_raw = str(r[12]).strip().lower() if r[12] is not None else 'desconocido'
    if sex_raw in ('mujer', 'mujeres'): s_id = 1
    elif sex_raw in ('hombre', 'hombres'): s_id = 0
    else: s_id = 2

    act_raw = str(r[2]).strip().upper() if r[2] is not None else 'DESCONOCIDO'
    if 'AUTOCONSUMO' in act_raw: a_id = 0
    elif 'MERCADO' in act_raw: a_id = 1
    else: a_id = 2

    atp_raw = str(r[15]).strip().upper() if r[15] is not None else 'NO'
    is_atp = 1 if ('BAI' in atp_raw or 'SI' in atp_raw or atp_raw == 'ATP') else 0

    ote = str(r[7] or r[8] or 'NO CLASIFICADA').strip()
    adr = str(r[18] or 'DESCONOCIDA').strip()
    muni = str(r[10] or 'DESCONOCIDO').strip().title()
    edad = int(r[11]) if isinstance(r[11], (int, float)) and 0 < r[11] < 120 else 0
    sup = round(float(r[14]), 2) if isinstance(r[14], (int, float)) and r[14] >= 0 else 0.0
    utas = round(float(r[17]), 2) if isinstance(r[17], (int, float)) and r[17] >= 0 else 0.0

    eco_raw = str(r[19] or 'NO').strip().lower()
    eco = 1 if ('cert' in eco_raw or 'proceso' in eco_raw or (eco_raw not in ('no', 'none', '') and len(eco_raw) > 2)) else 0

    jur = str(r[6] or 'Persona física').strip()

    ote_u = ote.upper()
    if 'BOVINO' in ote_u and 'LECHE' in ote_u: grp = 'Bovino Leche'
    elif 'BOVINO' in ote_u: grp = 'Bovino Carne'
    elif 'OVINO' in ote_u: grp = 'Ovino'
    elif 'CAPRINO' in ote_u: grp = 'Caprino'
    elif 'HORTALIZA' in ote_u and 'INVERNADERO' in ote_u: grp = 'Huerta Invernadero'
    elif 'HORTALIZA' in ote_u: grp = 'Huerta Aire Libre'
    elif 'FRUT' in ote_u: grp = 'Fruticultura'
    elif 'VITI' in ote_u: grp = 'Viticultura'
    elif 'AVES' in ote_u or 'PONEDORA' in ote_u: grp = 'Avicultura'
    elif 'FLOR' in ote_u: grp = 'Floricultura'
    elif 'AP' in ote_u: grp = 'Apicultura'
    elif 'PORCINO' in ote_u: grp = 'Porcino'
    elif 'EQUIT' in ote_u or 'CABALL' in ote_u: grp = 'Equino'
    else: grp = 'Otras / Mixtas'

    adr_u = adr.upper()
    if 'ENKAR' in adr_u: adr_c = 'Enkarterrialde'
    elif 'JATA' in adr_u: adr_c = 'Jata Ondo'
    elif 'GORBEI' in adr_u: adr_c = 'Gorbeialde'
    elif 'URREM' in adr_u: adr_c = 'Urremendi'
    elif 'URKI' in adr_u: adr_c = 'Urkiola'
    elif 'LEA' in adr_u: adr_c = 'Lea-Artibai'
    else: adr_c = 'Otras'

    jur_u = jur.upper()
    if 'PERSONA F' in jur_u: jur_c = 'Persona física'
    elif 'COMUNIDAD' in jur_u: jur_c = 'Comunidad de bienes'
    elif 'CIVIL' in jur_u: jur_c = 'Sociedad civil'
    elif 'COMPARTIDA' in jur_u: jur_c = 'Titularidad compartida'
    elif 'LIMITADA' in jur_u: jur_c = 'Sociedad limitada'
    elif 'COOPERATIVA' in jur_u: jur_c = 'Cooperativa'
    else: jur_c = 'Otras'

    adr_id = get_id(adr_c, adrs)
    muni_id = get_id(muni, munis)
    grp_id = get_id(grp, grps)
    jur_id = get_id(jur_c, jurs)
    ote_id = get_id(ote, otes)

    records.append([idx, s_id, a_id, is_atp, adr_id, muni_id, grp_id, edad, sup, eco, jur_id, utas, ote_id])

payload = {
    'vocab': {'adrs': adrs, 'munis': munis, 'grps': grps, 'jurs': jurs, 'otes': otes},
    'data': records
}

payload_json = json.dumps(payload, ensure_ascii=False)
print(f"Extracted {len(records)} records. JSON size: {len(payload_json)/1024:.1f} KB")

# HTML Template
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Explorador Multidimensional del Agro de Bizkaia | Perspectiva de Género</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Chart.js 4.4.1 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {
      /* Institutional Colors */
      --foral-950: #061911;
      --foral-900: #0A2318;
      --foral-800: #123826;
      --foral-700: #1B4D36;
      --foral-600: #266B4B;
      --foral-500: #10B981;
      --foral-100: #E6F3EC;
      --foral-50:  #F4F9F6;

      /* Gender Colors */
      --mujer-primary: #E11D48;
      --mujer-dark: #BE123C;
      --mujer-light: #FFF1F2;
      --mujer-border: #FECDD3;

      --hombre-primary: #2563EB;
      --hombre-dark: #1D4ED8;
      --hombre-light: #EFF6FF;
      --hombre-border: #BFDBFE;

      /* Professional Segments */
      --atp-primary: #059669;
      --atp-light: #ECFDF5;
      --noatp-primary: #D97706;
      --noatp-light: #FFFBEB;

      /* Neutrals */
      --slate-900: #0F172A;
      --slate-800: #1E293B;
      --slate-700: #334155;
      --slate-600: #475569;
      --slate-500: #64748B;
      --slate-400: #94A3B8;
      --slate-300: #CBD5E1;
      --slate-200: #E2E8F0;
      --slate-100: #F1F5F9;
      --slate-50:  #F8FAFC;
      --white: #FFFFFF;

      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 8px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 20px -2px rgba(15, 23, 42, 0.08);
      --shadow-lg: 0 14px 36px -6px rgba(15, 23, 42, 0.12);
      --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #F8FAF9;
      color: var(--slate-800);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    h1, h2, h3, h4, h5, .font-heading {
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Top Institutional Header */
    .gov-bar {
      background: var(--foral-950);
      color: #FFFFFF;
      padding: 10px 24px;
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      position: sticky;
      top: 0;
      z-index: 1000;
    }

    .gov-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }

    .gov-emblem {
      width: 22px;
      height: 22px;
      fill: #10B981;
    }

    .gov-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-top {
      background: rgba(255, 255, 255, 0.12);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
    }

    .btn-top:hover {
      background: rgba(255, 255, 255, 0.22);
    }

    .btn-top.active {
      background: #FFFFFF;
      color: var(--foral-950);
      border-color: #FFFFFF;
    }

    /* Main Container */
    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 20px 80px 20px;
    }

    /* Hero Banner */
    .hero-box {
      background: linear-gradient(135deg, #0A2318 0%, #17422E 60%, #1F543B 100%);
      color: #FFFFFF;
      border-radius: var(--radius-lg);
      padding: 30px 36px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(8px);
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 12px;
      color: #A7F3D0;
    }

    .hero-title {
      font-size: 30px;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 8px;
    }

    .hero-desc {
      font-size: 15px;
      color: rgba(255, 255, 255, 0.88);
      max-width: 980px;
      line-height: 1.5;
    }

    /* Preset Quick Bar */
    .presets-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 20px;
      background: #FFFFFF;
      padding: 12px 18px;
      border-radius: var(--radius-md);
      border: 1px solid var(--slate-200);
      box-shadow: var(--shadow-sm);
    }

    .preset-label {
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--slate-500);
      margin-right: 6px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .preset-btn {
      background: var(--slate-100);
      border: 1px solid var(--slate-200);
      color: var(--slate-700);
      font-size: 12.5px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: var(--transition);
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }

    .preset-btn:hover {
      background: var(--foral-100);
      color: var(--foral-800);
      border-color: var(--foral-500);
    }

    .preset-btn.active {
      background: var(--foral-700);
      color: #FFFFFF;
      border-color: var(--foral-700);
      box-shadow: 0 2px 8px rgba(27, 77, 54, 0.25);
    }

    /* Full Filtering Board */
    .filters-board {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 24px;
    }

    .filters-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--slate-100);
      padding-bottom: 12px;
    }

    .filters-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--slate-900);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .filters-reset-btn {
      background: transparent;
      border: 1px solid var(--slate-200);
      color: var(--slate-600);
      font-size: 12px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: var(--transition);
    }

    .filters-reset-btn:hover {
      background: #FEE2E2;
      color: #DC2626;
      border-color: #FECDD3;
    }

    .filters-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
    }

    .filter-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .filter-item-label {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--slate-600);
      display: flex;
      justify-content: space-between;
    }

    .filter-select {
      background: #FFFFFF;
      border: 1px solid var(--slate-300);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
      font-size: 13px;
      color: var(--slate-800);
      font-family: inherit;
      outline: none;
      transition: var(--transition);
      cursor: pointer;
    }

    .filter-select:focus {
      border-color: var(--foral-600);
      box-shadow: 0 0 0 3px rgba(38, 107, 75, 0.15);
    }

    /* Primary Segment Selectors (Sex, Activity, ATP) */
    .filter-item.primary-segment .filter-select {
      font-weight: 700;
      background: var(--slate-50);
      border-color: var(--slate-400);
    }

    /* KPI Ribbon */
    .kpi-ribbon {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }

    .kpi-tile {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
    }

    .kpi-tile:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .kpi-tile-lbl {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--slate-500);
      margin-bottom: 4px;
    }

    .kpi-tile-val {
      font-size: 24px;
      font-weight: 800;
      color: var(--slate-900);
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .kpi-tile-sub {
      font-size: 11.5px;
      color: var(--slate-600);
      margin-top: 2px;
    }

    /* Special Accent KPIs */
    .kpi-tile.kpi-mujeres {
      border-left: 4px solid var(--mujer-primary);
      background: linear-gradient(180deg, rgba(255, 241, 242, 0.5) 0%, #FFFFFF 100%);
    }
    .kpi-tile.kpi-mujeres .kpi-tile-val { color: var(--mujer-dark); }

    .kpi-tile.kpi-hombres {
      border-left: 4px solid var(--hombre-primary);
      background: linear-gradient(180deg, rgba(239, 246, 255, 0.5) 0%, #FFFFFF 100%);
    }

    .kpi-tile.kpi-atp {
      border-left: 4px solid var(--atp-primary);
    }

    /* DYNAMIC INSIGHT CARD (GENDER PERSPECTIVE) */
    .dynamic-insight-card {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-lg);
      padding: 26px 30px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
      border-left: 6px solid var(--foral-700);
    }

    .insight-topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .insight-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--foral-100);
      color: var(--foral-800);
      font-size: 12px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }

    .insight-selection-text {
      font-size: 13px;
      color: var(--slate-600);
      font-weight: 600;
    }

    .insight-headline {
      font-size: 21px;
      font-weight: 800;
      color: var(--slate-900);
      margin-bottom: 10px;
      line-height: 1.35;
    }

    .insight-summary-p {
      font-size: 15px;
      color: var(--slate-700);
      line-height: 1.6;
      margin-bottom: 18px;
    }

    .insight-findings-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      background: var(--slate-50);
      padding: 16px 20px;
      border-radius: var(--radius-md);
      border: 1px solid var(--slate-200);
    }

    .finding-col {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .finding-title {
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--foral-800);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .finding-desc {
      font-size: 13px;
      color: var(--slate-600);
      line-height: 1.45;
    }

    /* Micro Charts Section */
    .micro-charts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      gap: 18px;
      margin-bottom: 28px;
    }

    .chart-card {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-sm);
    }

    .chart-card-header {
      font-size: 13px;
      font-weight: 700;
      color: var(--slate-900);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chart-box {
      height: 200px;
      position: relative;
    }

    /* Table Explorer Section */
    .table-section {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }

    .table-controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .search-input {
      background: #FFFFFF;
      border: 1px solid var(--slate-300);
      border-radius: var(--radius-sm);
      padding: 8px 14px;
      font-size: 13px;
      width: 320px;
      outline: none;
      transition: var(--transition);
    }

    .search-input:focus {
      border-color: var(--foral-600);
      box-shadow: 0 0 0 3px rgba(38, 107, 75, 0.15);
    }

    .table-view-toggle {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-toggle-view {
      background: var(--slate-100);
      border: 1px solid var(--slate-200);
      color: var(--slate-700);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }

    .btn-toggle-view.active {
      background: var(--mujer-primary);
      color: #FFFFFF;
      border-color: var(--mujer-primary);
    }

    .data-table-wrap {
      overflow-x: auto;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-sm);
      max-height: 480px;
    }

    .table-explorer {
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }

    .table-explorer th {
      background: var(--slate-100);
      color: var(--slate-700);
      font-weight: 700;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--slate-200);
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .table-explorer td {
      padding: 8px 12px;
      border-bottom: 1px solid var(--slate-100);
      color: var(--slate-800);
    }

    .table-explorer tr:hover td {
      background: var(--slate-50);
    }

    /* Sex Pill Badges */
    .sex-pill {
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
    }
    .sex-pill.mujer { background: var(--mujer-light); color: var(--mujer-dark); border: 1px solid var(--mujer-border); }
    .sex-pill.hombre { background: var(--hombre-light); color: var(--hombre-dark); border: 1px solid var(--hombre-border); }
    .sex-pill.otro { background: var(--slate-100); color: var(--slate-600); }

    .tag-atp {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10.5px;
      font-weight: 700;
      background: var(--atp-light);
      color: var(--atp-primary);
    }

    .tag-noatp {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10.5px;
      font-weight: 700;
      background: var(--noatp-light);
      color: var(--noatp-primary);
    }

    /* Pagination */
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
      font-size: 12.5px;
      color: var(--slate-600);
    }

    .pagination-controls {
      display: flex;
      gap: 6px;
    }

    .page-btn {
      background: #FFFFFF;
      border: 1px solid var(--slate-300);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      transition: var(--transition);
    }

    .page-btn:hover:not(:disabled) {
      background: var(--slate-100);
    }

    .page-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Footer */
    footer.gov-footer {
      background: var(--foral-950);
      color: rgba(255, 255, 255, 0.7);
      padding: 30px 24px;
      font-size: 12.5px;
      margin-top: 60px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer-content {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    @media (max-width: 1200px) {
      .kpi-ribbon { grid-template-columns: repeat(3, 1fr); }
      .micro-charts-grid { grid-template-columns: 1fr 1fr; }
      .insight-findings-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 768px) {
      .kpi-ribbon { grid-template-columns: repeat(2, 1fr); }
      .micro-charts-grid { grid-template-columns: 1fr; }
      .filters-grid { grid-template-columns: 1fr; }
      .search-input { width: 100%; }
    }
  </style>
</head>

<body>

  <!-- TOP BAR -->
  <header class="gov-bar">
    <div class="gov-brand">
      <svg class="gov-emblem" viewBox="0 0 24 24">
        <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm1 14.5h-2v-2h2v2zm0-4h-2V7h2v5.5z"/>
      </svg>
      <span>BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA</span>
    </div>
    <div class="gov-actions">
      <a href="visor_mujeres_agro_bizkaia.html" class="btn-top">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        <span>Volver al Visor de Informe</span>
      </a>
      <button class="btn-top" onclick="exportFilteredCSV()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="7 10 12 15 17 10"></polyline>
          <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        <span>Exportar Selección (CSV)</span>
      </button>
      <button class="btn-top" onclick="window.print()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 6 2 18 2 18 9"></polyline>
          <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
          <rect x="6" y="14" width="12" height="8"></rect>
        </svg>
        <span>Imprimir</span>
      </button>
    </div>
  </header>

  <main class="container">

    <!-- HERO BOX -->
    <section class="hero-box">
      <div class="hero-badge">
        <span>HERRAMIENTA ANALÍTICA DINÁMICA · OBSERVATORIO AGRARIO DE BIZKAIA · AMATERRA</span>
      </div>
      <h1 class="hero-title">
        Explorador Multidimensional del Agro de Bizkaia
      </h1>
      <p class="hero-desc">
        Consulta y filtra en tiempo real sobre el censo oficial completo (12.650 explotaciones forales). Desgrana el sector desde el estrato macro hasta el microdato, con un <strong>motor analítico automático que genera diagnósticos con perspectiva de género</strong> al cambiar cualquier parámetro.
      </p>
    </section>

    <!-- PRESETS QUICK BAR -->
    <section class="presets-bar">
      <div class="preset-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <span>Vistas Rápidas:</span>
      </div>
      <button class="preset-btn active" id="preset-all" onclick="applyPreset('all')">
        <span>🔄 Todo el Censo (12.650)</span>
      </button>
      <button class="preset-btn" id="preset-fm-women" onclick="applyPreset('fm-women')">
        <span>🌟 1.194 Mujeres de Mercado</span>
      </button>
      <button class="preset-btn" id="preset-atp-women" onclick="applyPreset('atp-women')">
        <span>⚡ 190 Mujeres ATP (Profesionales)</span>
      </button>
      <button class="preset-btn" id="preset-auto-women" onclick="applyPreset('auto-women')">
        <span>🏡 2.470 Mujeres Autoconsumo</span>
      </button>
      <button class="preset-btn" id="preset-old-women" onclick="applyPreset('old-women')">
        <span>👵 Alerta Relevo: Mujeres >65 años</span>
      </button>
      <button class="preset-btn" id="preset-eco-women" onclick="applyPreset('eco-women')">
        <span>🌱 Mujeres en Ecológico</span>
      </button>
      <button class="preset-btn" id="preset-bov-enkarterri" onclick="applyPreset('bov-enkarterri')">
        <span>🏔️ Ganadería Enkarterri</span>
      </button>
      <button class="preset-btn" id="preset-horta-uribe" onclick="applyPreset('horta-uribe')">
        <span>🥕 Huerta Uribe / Jata Ondo</span>
      </button>
    </section>

    <!-- FILTERS BOARD -->
    <section class="filters-board">
      <div class="filters-header">
        <div class="filters-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          <span>Filtros Multidimensionales Cruzados</span>
        </div>
        <button class="filters-reset-btn" onclick="resetFilters()">
          <span>↺ Limpiar Filtros</span>
        </button>
      </div>

      <div class="filters-grid">
        <!-- Sexo -->
        <div class="filter-item primary-segment">
          <div class="filter-item-label">
            <span>1. Sexo Titular</span>
            <span id="badge-count-sex"></span>
          </div>
          <select id="flt-sexo" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Ambos Sexos (Censo Completo)</option>
            <option value="Mujer">Solo Mujeres</option>
            <option value="Hombre">Solo Hombres</option>
          </select>
        </div>

        <!-- Destino Actividad -->
        <div class="filter-item primary-segment">
          <div class="filter-item-label">
            <span>2. Destino Actividad</span>
          </div>
          <select id="flt-act" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todo Tipo de Actividad</option>
            <option value="Fines de mercado">Fines de Mercado (Comerciales)</option>
            <option value="Autoconsumo">Autoconsumo (Doméstico)</option>
            <option value="Otra">Otras Actividades</option>
          </select>
        </div>

        <!-- Régimen ATP -->
        <div class="filter-item primary-segment">
          <div class="filter-item-label">
            <span>3. Calificación ATP</span>
          </div>
          <select id="flt-atp" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todos los Regímenes</option>
            <option value="ATP">Solo ATP (Profesionales)</option>
            <option value="NO ATP">Solo NO ATP (Complementarias)</option>
          </select>
        </div>

        <!-- Comarca (ADR) -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>4. Comarca (ADR)</span>
          </div>
          <select id="flt-adr" class="filter-select" onchange="updateMunicipalityDropdown(); runFilterEngine();">
            <option value="ALL">Todas las Comarcas</option>
            <option value="Enkarterrialde">Enkarterrialde</option>
            <option value="Jata Ondo">Jata Ondo (Uribe)</option>
            <option value="Gorbeialde">Gorbeialde</option>
            <option value="Urremendi">Urremendi (Busturialdea)</option>
            <option value="Urkiola">Urkiola (Durangaldea)</option>
            <option value="Lea-Artibai">Lea-Artibai</option>
          </select>
        </div>

        <!-- Municipio -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>5. Municipio</span>
          </div>
          <select id="flt-muni" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todos los Municipios</option>
            <!-- Populated dynamically based on comarca -->
          </select>
        </div>

        <!-- Orientación Productiva (OTE) -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>6. Orientación Productiva</span>
          </div>
          <select id="flt-grp" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todos los Subsectores</option>
            <option value="Bovino Carne">Bovino Carne</option>
            <option value="Bovino Leche">Bovino Leche</option>
            <option value="Ovino">Ovino</option>
            <option value="Huerta Invernadero">Huerta Invernadero</option>
            <option value="Huerta Aire Libre">Huerta Aire Libre</option>
            <option value="Fruticultura">Fruticultura</option>
            <option value="Viticultura">Viticultura (Txakoli)</option>
            <option value="Avicultura">Avicultura</option>
            <option value="Caprino">Caprino</option>
            <option value="Equino">Equino</option>
            <option value="Floricultura">Floricultura</option>
            <option value="Apicultura">Apicultura</option>
            <option value="Porcino">Porcino</option>
            <option value="Otras / Mixtas">Otras / Mixtas</option>
          </select>
        </div>

        <!-- Tramo de Edad -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>7. Tramo de Edad</span>
          </div>
          <select id="flt-edad" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todas las Edades</option>
            <option value="18-40">18 - 40 años (Jóvenes)</option>
            <option value="41-65">41 - 65 años (Maduras)</option>
            <option value=">65">> 65 años (Jubilación)</option>
          </select>
        </div>

        <!-- Tramo de Superficie -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>8. Superficie (ha)</span>
          </div>
          <select id="flt-sup" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Cualquier Superficie</option>
            <option value="<5">Muy pequeña: 0,5 - 5 ha</option>
            <option value="5-20">Pequeña: 5 - 20 ha</option>
            <option value="20-50">Mediana: 20 - 50 ha</option>
            <option value=">50">Grande: > 50 ha</option>
          </select>
        </div>

        <!-- Modelo Ecológico -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>9. Certificación Eco</span>
          </div>
          <select id="flt-eco" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Ecológico y Convencional</option>
            <option value="SI">Solo Certificado / Proceso Eco</option>
            <option value="NO">Solo Convencional</option>
          </select>
        </div>

        <!-- Forma Jurídica -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>10. Forma Jurídica</span>
          </div>
          <select id="flt-jur" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Todas las Formas</option>
            <option value="Persona física">Persona física</option>
            <option value="Comunidad de bienes">Comunidad de bienes</option>
            <option value="Sociedad civil">Sociedad civil</option>
            <option value="Titularidad compartida">Titularidad compartida</option>
            <option value="Sociedad limitada">Sociedad limitada</option>
            <option value="Cooperativa">Cooperativa</option>
            <option value="Otras">Otras</option>
          </select>
        </div>

        <!-- Dedicación UTAs -->
        <div class="filter-item">
          <div class="filter-item-label">
            <span>11. Dedicación UTAs</span>
          </div>
          <select id="flt-utas" class="filter-select" onchange="runFilterEngine()">
            <option value="ALL">Cualquier Carga Laboral</option>
            <option value=">=1">Tiempo Completo (>= 1 UTA)</option>
            <option value="<1">Tiempo Parcial (< 1 UTA)</option>
          </select>
        </div>
      </div>
    </section>

    <!-- KPI RIBBON -->
    <section class="kpi-ribbon">
      <div class="kpi-tile">
        <div class="kpi-tile-lbl">Total Filtrado</div>
        <div class="kpi-tile-val" id="kpi-total">12.650</div>
        <div class="kpi-tile-sub" id="kpi-total-sub">100% del censo</div>
      </div>

      <div class="kpi-tile kpi-mujeres">
        <div class="kpi-tile-lbl">Mujeres Titulares</div>
        <div class="kpi-tile-val" id="kpi-mujeres">3.723</div>
        <div class="kpi-tile-sub" id="kpi-mujeres-pct">29,4% de cuota</div>
      </div>

      <div class="kpi-tile kpi-hombres">
        <div class="kpi-tile-lbl">Hombres Titulares</div>
        <div class="kpi-tile-val" id="kpi-hombres">8.791</div>
        <div class="kpi-tile-sub" id="kpi-hombres-pct">69,5% de cuota</div>
      </div>

      <div class="kpi-tile kpi-atp">
        <div class="kpi-tile-lbl">Profesionales ATP</div>
        <div class="kpi-tile-val" id="kpi-atp">529</div>
        <div class="kpi-tile-sub" id="kpi-atp-sub">190 mujeres (35,9%)</div>
      </div>

      <div class="kpi-tile">
        <div class="kpi-tile-lbl">Edad Media Mujeres</div>
        <div class="kpi-tile-val" id="kpi-edad-m">64,5 a.</div>
        <div class="kpi-tile-sub" id="kpi-edad-diff">vs 61,2 a. hombres</div>
      </div>

      <div class="kpi-tile">
        <div class="kpi-tile-lbl">Superficie Media M.</div>
        <div class="kpi-tile-val" id="kpi-sup-m">8,4 ha</div>
        <div class="kpi-tile-sub" id="kpi-sup-diff">vs 11,8 ha hombres</div>
      </div>
    </section>

    <!-- DYNAMIC INSIGHT CARD (GENDER PERSPECTIVE ENGINE) -->
    <section class="dynamic-insight-card" id="dynamic-insight-box">
      <div class="insight-topbar">
        <div class="insight-badge-pill">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span>Diagnóstico Automático · Perspectiva de Género</span>
        </div>
        <div class="insight-selection-text" id="ins-selection-summary">
          Segmento actual: Censo Agrario Total de Bizkaia
        </div>
      </div>

      <h2 class="insight-headline" id="ins-headline">
        Censo Global: 3 de cada 10 explotaciones forales están a nombre de mujeres
      </h2>
      <p class="insight-summary-p" id="ins-summary-text">
        El conjunto del registro foral muestra una tasa de titularidad femenina del <strong>29,4% (3.723 mujeres)</strong>. Al desglosar los filtros por destino económico y profesionalización, se aprecian contrastes estructurales inmediatos en envejecimiento y tamaño de la explotación.
      </p>

      <div class="insight-findings-grid">
        <div class="finding-col">
          <div class="finding-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Brecha de Edad y Relevo</span>
          </div>
          <div class="finding-desc" id="ins-finding-age">
            Cargando análisis de edad...
          </div>
        </div>

        <div class="finding-col">
          <div class="finding-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
            <span>Brecha de Tierra y Escala</span>
          </div>
          <div class="finding-desc" id="ins-finding-land">
            Cargando análisis territorial...
          </div>
        </div>

        <div class="finding-col">
          <div class="finding-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2a9 9 0 0 0-9 9c0 4.97 4.03 9 9 9 4.97 0 9-4.03 9-9 0-4.97-4.03-9-9-9z"/></svg>
            <span>Modelo Agroecológico y Dedicación</span>
          </div>
          <div class="finding-desc" id="ins-finding-eco">
            Cargando análisis de sostenibilidad...
          </div>
        </div>
      </div>
    </section>

    <!-- MICRO CHARTS GRID -->
    <section class="micro-charts-grid">
      <!-- Gender Donut -->
      <div class="chart-card">
        <div class="chart-card-header">
          <span>Balanza de Sexo en Selección</span>
        </div>
        <div class="chart-box">
          <canvas id="chartMiniGender"></canvas>
        </div>
      </div>

      <!-- Age Pyramid -->
      <div class="chart-card">
        <div class="chart-card-header">
          <span>Pirámide de Edad (Mujeres vs Hombres)</span>
        </div>
        <div class="chart-box">
          <canvas id="chartMiniAge"></canvas>
        </div>
      </div>

      <!-- Land Size -->
      <div class="chart-card">
        <div class="chart-card-header">
          <span>Estrato de Superficie</span>
        </div>
        <div class="chart-box">
          <canvas id="chartMiniSup"></canvas>
        </div>
      </div>

      <!-- Top Sectors -->
      <div class="chart-card">
        <div class="chart-card-header">
          <span>Top Orientaciones (Mujeres)</span>
        </div>
        <div class="chart-box">
          <canvas id="chartMiniSector"></canvas>
        </div>
      </div>
    </section>

    <!-- TABLE SECTION -->
    <section class="table-section">
      <div class="table-controls">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
          <input type="text" id="table-search" class="search-input" 
                 placeholder="Buscar por municipio, comarca o subsector..." 
                 oninput="runFilterEngine()">
          <span id="table-count-label" style="font-size:12.5px; font-weight:700; color:var(--slate-600);">
            Mostrando 12.650 registros
          </span>
        </div>

        <div class="table-view-toggle">
          <button class="btn-toggle-view active" id="btn-show-all-sex" onclick="setTableViewMode('all')">
            <span>Todos en Selección</span>
          </button>
          <button class="btn-toggle-view" id="btn-show-only-women" onclick="setTableViewMode('women')">
            <span>Solo Registros de Mujeres</span>
          </button>
        </div>
      </div>

      <div class="data-table-wrap">
        <table class="table-explorer">
          <thead>
            <tr>
              <th>ID</th>
              <th>Sexo</th>
              <th>Destino Actividad</th>
              <th>Régimen</th>
              <th>Municipio</th>
              <th>Comarca</th>
              <th>Orientación (OTE)</th>
              <th>Edad</th>
              <th>Superficie</th>
              <th>Eco</th>
              <th>Forma Jurídica</th>
              <th>UTAs</th>
            </tr>
          </thead>
          <tbody id="table-body">
            <!-- Dynamic Rows -->
          </tbody>
        </table>
      </div>

      <div class="pagination-bar">
        <div>
          <span>Página <strong id="cur-page">1</strong> de <strong id="total-pages">1</strong></span>
        </div>
        <div class="pagination-controls">
          <button class="page-btn" id="btn-prev-page" onclick="changePage(-1)">← Anterior</button>
          <button class="page-btn" id="btn-next-page" onclick="changePage(1)">Siguiente →</button>
        </div>
      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="gov-footer">
    <div class="footer-content">
      <div>
        <div style="font-weight:700; color:#FFFFFF; margin-bottom:2px;">
          Diputación Foral de Bizkaia · Bizkaiko Foru Aldundia
        </div>
        <div>Departamento de Medio Natural y Agricultura · Nekazaritza eta Natura Ingurune Saila</div>
      </div>
      <div style="text-align:right;">
        <div>Estudio y Visor Dinámico desarrollado por <strong>Amaterra</strong></div>
        <div style="font-size:11.5px; opacity:0.75;">Censo Oficial de Explotaciones Agrarias de Bizkaia · Septiembre 2026</div>
      </div>
    </div>
  </footer>

  <!-- SCRIPT DATA & ENGINE -->
  <script>
    // Embedded compressed database
    const BUNDLE = """ + payload_json + """;
    const VOCAB = BUNDLE.vocab;
    const DATA = BUNDLE.data;

    // Charts instances
    let charts = {};
    let filteredData = DATA;
    let tableMode = 'all'; // 'all' or 'women'
    let currentPage = 1;
    const pageSize = 50;

    // Initialize on load
    window.addEventListener('DOMContentLoaded', () => {
      initDropdowns();
      initCharts();
      runFilterEngine();
    });

    function initDropdowns() {
      const muniSelect = document.getElementById('flt-muni');
      const sortedMunis = [...VOCAB.munis].sort((a,b) => a.localeCompare(b));
      sortedMunis.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.textContent = m;
        muniSelect.appendChild(opt);
      });
    }

    function updateMunicipalityDropdown() {
      const selAdr = document.getElementById('flt-adr').value;
      const muniSelect = document.getElementById('flt-muni');
      const currentMuni = muniSelect.value;

      muniSelect.innerHTML = '<option value="ALL">Todos los Municipios</option>';

      let validMunis = new Set();
      DATA.forEach(r => {
        const adrName = VOCAB.adrs[r[4]];
        if (selAdr === 'ALL' || adrName === selAdr) {
          validMunis.add(VOCAB.munis[r[5]]);
        }
      });

      const sortedMunis = Array.from(validMunis).sort((a,b) => a.localeCompare(b));
      sortedMunis.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.textContent = m;
        if (m === currentMuni) opt.selected = true;
        muniSelect.appendChild(opt);
      });
    }

    // Preset Buttons
    function applyPreset(presetKey) {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`preset-${presetKey}`);
      if (activeBtn) activeBtn.classList.add('active');

      resetFilterInputsOnly();

      if (presetKey === 'fm-women') {
        document.getElementById('flt-sexo').value = 'Mujer';
        document.getElementById('flt-act').value = 'Fines de mercado';
      } else if (presetKey === 'atp-women') {
        document.getElementById('flt-sexo').value = 'Mujer';
        document.getElementById('flt-act').value = 'Fines de mercado';
        document.getElementById('flt-atp').value = 'ATP';
      } else if (presetKey === 'auto-women') {
        document.getElementById('flt-sexo').value = 'Mujer';
        document.getElementById('flt-act').value = 'Autoconsumo';
      } else if (presetKey === 'old-women') {
        document.getElementById('flt-sexo').value = 'Mujer';
        document.getElementById('flt-act').value = 'Fines de mercado';
        document.getElementById('flt-edad').value = '>65';
      } else if (presetKey === 'eco-women') {
        document.getElementById('flt-sexo').value = 'Mujer';
        document.getElementById('flt-eco').value = 'SI';
      } else if (presetKey === 'bov-enkarterri') {
        document.getElementById('flt-adr').value = 'Enkarterrialde';
        document.getElementById('flt-grp').value = 'Bovino Carne';
      } else if (presetKey === 'horta-uribe') {
        document.getElementById('flt-adr').value = 'Jata Ondo';
        document.getElementById('flt-grp').value = 'Huerta Invernadero';
      }

      runFilterEngine();
    }

    function resetFilterInputsOnly() {
      document.getElementById('flt-sexo').value = 'ALL';
      document.getElementById('flt-act').value = 'ALL';
      document.getElementById('flt-atp').value = 'ALL';
      document.getElementById('flt-adr').value = 'ALL';
      document.getElementById('flt-muni').value = 'ALL';
      document.getElementById('flt-grp').value = 'ALL';
      document.getElementById('flt-edad').value = 'ALL';
      document.getElementById('flt-sup').value = 'ALL';
      document.getElementById('flt-eco').value = 'ALL';
      document.getElementById('flt-jur').value = 'ALL';
      document.getElementById('flt-utas').value = 'ALL';
      document.getElementById('table-search').value = '';
    }

    function resetFilters() {
      resetFilterInputsOnly();
      applyPreset('all');
    }

    function setTableViewMode(mode) {
      tableMode = mode;
      document.getElementById('btn-show-all-sex').classList.toggle('active', mode === 'all');
      document.getElementById('btn-show-only-women').classList.toggle('active', mode === 'women');
      currentPage = 1;
      renderTable();
    }

    // MAIN FILTERING AND CALCULATION ENGINE
    function runFilterEngine() {
      const fSex = document.getElementById('flt-sexo').value;
      const fAct = document.getElementById('flt-act').value;
      const fAtp = document.getElementById('flt-atp').value;
      const fAdr = document.getElementById('flt-adr').value;
      const fMuni = document.getElementById('flt-muni').value;
      const fGrp = document.getElementById('flt-grp').value;
      const fEdad = document.getElementById('flt-edad').value;
      const fSup = document.getElementById('flt-sup').value;
      const fEco = document.getElementById('flt-eco').value;
      const fJur = document.getElementById('flt-jur').value;
      const fUtas = document.getElementById('flt-utas').value;
      const fSearch = (document.getElementById('table-search').value || '').toLowerCase().trim();

      filteredData = DATA.filter(r => {
        // Sex: 1=Mujer, 0=Hombre, 2=Otro
        if (fSex === 'Mujer' && r[1] !== 1) return false;
        if (fSex === 'Hombre' && r[1] !== 0) return false;

        // Act: 0=Autoconsumo, 1=Mercado, 2=Otra
        if (fAct === 'Autoconsumo' && r[2] !== 0) return false;
        if (fAct === 'Fines de mercado' && r[2] !== 1) return false;
        if (fAct === 'Otra' && r[2] !== 2) return false;

        // ATP: 1=ATP, 0=NO ATP
        if (fAtp === 'ATP' && r[3] !== 1) return false;
        if (fAtp === 'NO ATP' && r[3] !== 0) return false;

        // ADR
        if (fAdr !== 'ALL' && VOCAB.adrs[r[4]] !== fAdr) return false;

        // Muni
        if (fMuni !== 'ALL' && VOCAB.munis[r[5]] !== fMuni) return false;

        // Grp
        if (fGrp !== 'ALL' && VOCAB.grps[r[6]] !== fGrp) return false;

        // Edad
        const age = r[7];
        if (fEdad === '18-40' && (age <= 0 || age > 40)) return false;
        if (fEdad === '41-65' && (age < 41 || age > 65)) return false;
        if (fEdad === '>65' && age <= 65) return false;

        // Sup
        const s = r[8];
        if (fSup === '<5' && (s < 0.5 || s >= 5)) return false;
        if (fSup === '5-20' && (s < 5 || s >= 20)) return false;
        if (fSup === '20-50' && (s < 20 || s >= 50)) return false;
        if (fSup === '>50' && s < 50) return false;

        // Eco: 1=SI, 0=NO
        if (fEco === 'SI' && r[9] !== 1) return false;
        if (fEco === 'NO' && r[9] !== 0) return false;

        // Jur
        if (fJur !== 'ALL' && VOCAB.jurs[r[10]] !== fJur) return false;

        // UTAs
        const u = r[11];
        if (fUtas === '>=1' && u < 1) return false;
        if (fUtas === '<1' && u >= 1) return false;

        // Text Search
        if (fSearch) {
          const hay = `${VOCAB.munis[r[5]]} ${VOCAB.adrs[r[4]]} ${VOCAB.otes[r[12]]} ${VOCAB.grps[r[6]]}`.toLowerCase();
          if (!hay.includes(fSearch)) return false;
        }

        return true;
      });

      // Update KPIs & Analytics
      updateKPIsAndInsights();
      updateCharts();
      currentPage = 1;
      renderTable();
    }

    function updateKPIsAndInsights() {
      const total = filteredData.length;
      const womenRows = filteredData.filter(r => r[1] === 1);
      const menRows = filteredData.filter(r => r[1] === 0);
      const otherRows = filteredData.filter(r => r[1] === 2);

      const countW = womenRows.length;
      const countM = menRows.length;
      const pctW = total > 0 ? ((countW / total) * 100).toFixed(1) : 0;
      const pctM = total > 0 ? ((countM / total) * 100).toFixed(1) : 0;

      const atpRows = filteredData.filter(r => r[3] === 1);
      const atpWomen = atpRows.filter(r => r[1] === 1).length;
      const atpTotal = atpRows.length;

      // Ages
      const validAgesW = womenRows.map(r => r[7]).filter(a => a > 0);
      const avgAgeW = validAgesW.length > 0 ? (validAgesW.reduce((a,b)=>a+b,0)/validAgesW.length).toFixed(1) : '-';

      const validAgesM = menRows.map(r => r[7]).filter(a => a > 0);
      const avgAgeM = validAgesM.length > 0 ? (validAgesM.reduce((a,b)=>a+b,0)/validAgesM.length).toFixed(1) : '-';

      // Surfaces
      const validSupW = womenRows.map(r => r[8]).filter(s => s > 0);
      const avgSupW = validSupW.length > 0 ? (validSupW.reduce((a,b)=>a+b,0)/validSupW.length).toFixed(1) : '-';

      const validSupM = menRows.map(r => r[8]).filter(s => s > 0);
      const avgSupM = validSupM.length > 0 ? (validSupM.reduce((a,b)=>a+b,0)/validSupM.length).toFixed(1) : '-';

      // Eco
      const ecoW = womenRows.filter(r => r[9] === 1).length;
      const ecoM = menRows.filter(r => r[9] === 1).length;

      // Update KPI tiles
      document.getElementById('kpi-total').textContent = total.toLocaleString('es-ES');
      document.getElementById('kpi-total-sub').textContent = `${((total/12650)*100).toFixed(1)}% del censo total`;

      document.getElementById('kpi-mujeres').textContent = countW.toLocaleString('es-ES');
      document.getElementById('kpi-mujeres-pct').textContent = `${pctW}% del segmento filtrado`;

      document.getElementById('kpi-hombres').textContent = countM.toLocaleString('es-ES');
      document.getElementById('kpi-hombres-pct').textContent = `${pctM}% del segmento filtrado`;

      document.getElementById('kpi-atp').textContent = atpTotal.toLocaleString('es-ES');
      document.getElementById('kpi-atp-sub').textContent = atpTotal > 0 ? `${atpWomen} mujeres (${((atpWomen/atpTotal)*100).toFixed(1)}%)` : '0 mujeres';

      document.getElementById('kpi-edad-m').textContent = avgAgeW !== '-' ? `${avgAgeW} a.` : '-';
      document.getElementById('kpi-edad-diff').textContent = avgAgeM !== '-' ? `vs ${avgAgeM} a. hombres` : '-';

      document.getElementById('kpi-sup-m').textContent = avgSupW !== '-' ? `${avgSupW} ha` : '-';
      document.getElementById('kpi-sup-diff').textContent = avgSupM !== '-' ? `vs ${avgSupM} ha hombres` : '-';

      // BUILD DYNAMIC GENDER INSIGHT TEXT
      buildDynamicInsight({
        total, countW, countM, pctW, pctM,
        atpTotal, atpWomen,
        validAgesW, avgAgeW, avgAgeM,
        validSupW, avgSupW, avgSupM,
        ecoW, ecoM
      });
    }

    function buildDynamicInsight(metrics) {
      const fSex = document.getElementById('flt-sexo').value;
      const fAct = document.getElementById('flt-act').value;
      const fAtp = document.getElementById('flt-atp').value;
      const fAdr = document.getElementById('flt-adr').value;
      const fGrp = document.getElementById('flt-grp').value;
      const fEdad = document.getElementById('flt-edad').value;

      // Selection narrative text
      let selTerms = [];
      if (fSex !== 'ALL') selTerms.push(`Sexo: ${fSex}`);
      if (fAct !== 'ALL') selTerms.push(`Actividad: ${fAct}`);
      if (fAtp !== 'ALL') selTerms.push(`Régimen: ${fAtp}`);
      if (fAdr !== 'ALL') selTerms.push(`Comarca: ${fAdr}`);
      if (fGrp !== 'ALL') selTerms.push(`Sector: ${fGrp}`);
      if (fEdad !== 'ALL') selTerms.push(`Edad: ${fEdad}`);

      const selSummary = selTerms.length > 0 ? selTerms.join(' · ') : 'Censo Agrario Total de Bizkaia (Sin Filtros)';
      document.getElementById('ins-selection-summary').textContent = `Selección activa: ${selSummary}`;

      // Headline logic
      let headline = '';
      let summaryText = '';

      if (metrics.total === 0) {
        document.getElementById('ins-headline').textContent = 'No se han encontrado explotaciones con este cruce de filtros';
        document.getElementById('ins-summary-text').textContent = 'Prueba a relajar los parámetros para ampliar la muestra de análisis.';
        document.getElementById('ins-finding-age').textContent = 'Sin datos';
        document.getElementById('ins-finding-land').textContent = 'Sin datos';
        document.getElementById('ins-finding-eco').textContent = 'Sin datos';
        return;
      }

      const diffFromBaseline = (metrics.pctW - 30.2).toFixed(1);
      const isAboveBaseline = metrics.pctW > 30.2;

      if (fAct === 'Fines de mercado' && fSex === 'Mujer') {
        headline = `Las 1.194 Mujeres de Mercado: La Columna Vertebral Comercial del Agro Femenino`;
        summaryText = `Este colectivo representa el 35,9% de todas las explotaciones con fines de mercado de Bizkaia, superando en 5,7 puntos porcentuales la presencia de la mujer en el censo global foral. Constituyen las productoras sobre las que debe incidir cualquier política de desarrollo rural y relevo.`;
      } else if (fAtp === 'ATP') {
        headline = `Segmento Profesional ATP: Máxima Dedicación con un 35,9% de Liderazgo Femenino`;
        summaryText = `Entre los 529 profesionales a título principal de Bizkaia, 190 son mujeres. Este colectivo presenta un volumen laboral superior (media de 1,42 UTAs), mayor escala territorial y un compromiso agroambiental multiplicador.`;
      } else if (fAct === 'Autoconsumo') {
        headline = `El Ámbito del Autoconsumo: 2.470 Mujeres Mantienen Huertos Familiares de Recreo`;
        summaryText = `El autoconsumo representa la mayor bolsa de titulares rurales de Bizkaia. Aunque no comercializan producción en mercado, las mujeres gestionan el 28% de estos huertos familiares, claves para la soberanía alimentaria doméstica y la cohesión comunitaria.`;
      } else if (isAboveBaseline) {
        headline = `Sobre-Representación Femenina: La Cuota de Mujeres Sube al ${metrics.pctW}% (+${diffFromBaseline}% sobre la media)`;
        summaryText = `En esta selección específica, la presencia de la mujer es notablemente superior al promedio foral (30,2%), señalando un sector o comarca con especial vocación de emprendimiento agrario femenino.`;
      } else {
        headline = `Sub-Representación Femenina: Las Mujeres Aportan el ${metrics.pctW}% de la Titularidad (${diffFromBaseline}% vs media)`;
        summaryText = `En este corte del sector, la titularidad continúa fuertemente masculinizada (${metrics.pctM}% hombres), indicando posibles barreras de acceso histórico, transmisión patrimonial o dificultades de relevo para las mujeres.`;
      }

      document.getElementById('ins-headline').textContent = headline;
      document.getElementById('ins-summary-text').textContent = summaryText;

      // 1. Age finding
      const over65W = metrics.validAgesW.filter(a => a > 65).length;
      const pct65W = metrics.validAgesW.length > 0 ? ((over65W / metrics.validAgesW.length) * 100).toFixed(1) : 0;
      const youngW = metrics.validAgesW.filter(a => a <= 40).length;

      document.getElementById('ins-finding-age').innerHTML = `
        Edad media de las mujeres: <strong>${metrics.avgAgeW} años</strong> (hombres: ${metrics.avgAgeM} a.).
        El <strong>${pct65W}%</strong> (${over65W} mujeres) superan los 65 años, frente a solo <strong>${youngW} mujeres jóvenes</strong> (&le;40 a.).
      `;

      // 2. Land finding
      const microW = metrics.validSupW.filter(s => s < 5).length;
      const pctMicroW = metrics.validSupW.length > 0 ? ((microW / metrics.validSupW.length) * 100).toFixed(1) : 0;

      let landComp = '';
      if (metrics.avgSupM !== '-' && metrics.avgSupW !== '-') {
        const gap = (parseFloat(metrics.avgSupM) - parseFloat(metrics.avgSupW)).toFixed(1);
        landComp = gap > 0 ? `Brecha de género en superficie: los hombres gestionan de media <strong>+${gap} ha</strong> más que las mujeres.` : 'Superficie media femenina igual o superior a los hombres en este estrato.';
      }

      document.getElementById('ins-finding-land').innerHTML = `
        Superficie media en mujeres: <strong>${metrics.avgSupW} ha</strong>.
        El <strong>${pctMicroW}%</strong> de las mujeres gestionan minifundios de menos de 5 ha. ${landComp}
      `;

      // 3. Eco finding
      const totalEco = metrics.ecoW + metrics.ecoM;
      const ecoShareW = totalEco > 0 ? ((metrics.ecoW / totalEco) * 100).toFixed(1) : 0;

      document.getElementById('ins-finding-eco').innerHTML = `
        Explotaciones ecológicas en este corte: <strong>${metrics.ecoW} lideradas por mujeres</strong> (${ecoShareW}% del total eco).
        ${metrics.ecoW > 10 ? 'Demuestra una alta penetración del modelo sostenible en titulares femeninas.' : 'Representa un potencial de conversión ecológica para las líneas de ayuda forales.'}
      `;
    }

    // CHART ENGINE
    function initCharts() {
      // 1. Gender Donut
      const ctxG = document.getElementById('chartMiniGender').getContext('2d');
      charts.gender = new Chart(ctxG, {
        type: 'doughnut',
        data: {
          labels: ['Mujeres', 'Hombres'],
          datasets: [{
            data: [3723, 8791],
            backgroundColor: ['#E11D48', '#2563EB'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 11, weight: '600' } } }
          }
        }
      });

      // 2. Age Pyramid
      const ctxA = document.getElementById('chartMiniAge').getContext('2d');
      charts.age = new Chart(ctxA, {
        type: 'bar',
        data: {
          labels: ['18-40', '41-65', '>65'],
          datasets: [
            { label: 'Mujeres', data: [0, 0, 0], backgroundColor: '#E11D48', borderRadius: 4 },
            { label: 'Hombres', data: [0, 0, 0], backgroundColor: '#2563EB', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, grid: { color: '#F1F5F9' } },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
          }
        }
      });

      // 3. Surface Bars
      const ctxS = document.getElementById('chartMiniSup').getContext('2d');
      charts.sup = new Chart(ctxS, {
        type: 'bar',
        data: {
          labels: ['<5 ha', '5-20 ha', '20-50 ha', '>50 ha'],
          datasets: [
            { label: 'Mujeres', data: [0, 0, 0, 0], backgroundColor: '#E11D48', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, grid: { color: '#F1F5F9' } },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });

      // 4. Top Sectors
      const ctxSec = document.getElementById('chartMiniSector').getContext('2d');
      charts.sector = new Chart(ctxSec, {
        type: 'bar',
        data: {
          labels: ['Bov. Carne', 'Ovino', 'Huerta Inv.', 'Frutales'],
          datasets: [{
            label: 'Mujeres',
            data: [0, 0, 0, 0],
            backgroundColor: '#059669',
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { beginAtZero: true, grid: { color: '#F1F5F9' } },
            y: { grid: { display: false } }
          },
          plugins: { legend: { display: false } }
        }
      });
    }

    function updateCharts() {
      const womenRows = filteredData.filter(r => r[1] === 1);
      const menRows = filteredData.filter(r => r[1] === 0);

      // 1. Gender Donut
      charts.gender.data.datasets[0].data = [womenRows.length, menRows.length];
      charts.gender.update();

      // 2. Age
      const wAge1 = womenRows.filter(r => r[7] > 0 && r[7] <= 40).length;
      const wAge2 = womenRows.filter(r => r[7] >= 41 && r[7] <= 65).length;
      const wAge3 = womenRows.filter(r => r[7] > 65).length;

      const mAge1 = menRows.filter(r => r[7] > 0 && r[7] <= 40).length;
      const mAge2 = menRows.filter(r => r[7] >= 41 && r[7] <= 65).length;
      const mAge3 = menRows.filter(r => r[7] > 65).length;

      charts.age.data.datasets[0].data = [wAge1, wAge2, wAge3];
      charts.age.data.datasets[1].data = [mAge1, mAge2, mAge3];
      charts.age.update();

      // 3. Sup
      const wSup1 = womenRows.filter(r => r[8] > 0 && r[8] < 5).length;
      const wSup2 = womenRows.filter(r => r[8] >= 5 && r[8] < 20).length;
      const wSup3 = womenRows.filter(r => r[8] >= 20 && r[8] < 50).length;
      const wSup4 = womenRows.filter(r => r[8] >= 50).length;

      charts.sup.data.datasets[0].data = [wSup1, wSup2, wSup3, wSup4];
      charts.sup.update();

      // 4. Sector
      const sectorCounts = {};
      womenRows.forEach(r => {
        const grp = VOCAB.grps[r[6]];
        sectorCounts[grp] = (sectorCounts[grp] || 0) + 1;
      });

      const sortedSecs = Object.entries(sectorCounts).sort((a,b) => b[1] - a[1]).slice(0, 4);
      charts.sector.data.labels = sortedSecs.map(s => s[0]);
      charts.sector.data.datasets[0].data = sortedSecs.map(s => s[1]);
      charts.sector.update();
    }

    // TABLE PAGINATION & RENDERING
    function renderTable() {
      const displayData = tableMode === 'women' 
        ? filteredData.filter(r => r[1] === 1)
        : filteredData;

      const totalItems = displayData.length;
      const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;

      document.getElementById('cur-page').textContent = currentPage;
      document.getElementById('total-pages').textContent = totalPages;
      document.getElementById('btn-prev-page').disabled = (currentPage === 1);
      document.getElementById('btn-next-page').disabled = (currentPage === totalPages);

      document.getElementById('table-count-label').textContent = 
        `Mostrando ${totalItems.toLocaleString('es-ES')} explotaciones (${tableMode === 'women' ? 'solo mujeres' : 'todos los sexos'})`;

      const startIdx = (currentPage - 1) * pageSize;
      const pageRows = displayData.slice(startIdx, startIdx + pageSize);

      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      if (pageRows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="12" style="text-align:center; padding:24px; color:#94A3B8;">No se encontraron registros con los filtros actuales.</td></tr>';
        return;
      }

      pageRows.forEach(r => {
        const tr = document.createElement('tr');
        const sexName = r[1] === 1 ? 'Mujer' : (r[1] === 0 ? 'Hombre' : 'Otro');
        const sexClass = r[1] === 1 ? 'mujer' : (r[1] === 0 ? 'hombre' : 'otro');
        const actName = r[2] === 1 ? 'Mercado' : (r[2] === 0 ? 'Autoconsumo' : 'Otra');
        const atpTag = r[3] === 1 ? '<span class="tag-atp">ATP</span>' : '<span class="tag-noatp">No ATP</span>';
        const ecoBadge = r[9] === 1 ? '<span style="color:#059669; font-weight:700;">✓ Eco</span>' : '<span style="color:#94A3B8;">-</span>';

        tr.innerHTML = `
          <td><span style="color:#94A3B8; font-size:11px;">#${r[0]}</span></td>
          <td><span class="sex-pill ${sexClass}">${sexName}</span></td>
          <td><strong>${actName}</strong></td>
          <td>${atpTag}</td>
          <td>${VOCAB.munis[r[5]]}</td>
          <td>${VOCAB.adrs[r[4]]}</td>
          <td>${VOCAB.otes[r[12]]}</td>
          <td>${r[7] > 0 ? r[7] + ' a.' : '-'}</td>
          <td>${r[8] > 0 ? r[8] + ' ha' : '-'}</td>
          <td>${ecoBadge}</td>
          <td>${VOCAB.jurs[r[10]]}</td>
          <td><strong>${r[11]}</strong></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function changePage(delta) {
      currentPage += delta;
      renderTable();
    }

    // CSV EXPORT
    function exportFilteredCSV() {
      const headers = ['ID', 'Sexo', 'Actividad', 'Calificacion_ATP', 'Municipio', 'Comarca', 'Subsector_OTE', 'Edad', 'Superficie_ha', 'Ecologico', 'Forma_Juridica', 'UTAs'];
      const rows = filteredData.map(r => [
        r[0],
        r[1] === 1 ? 'Mujer' : (r[1] === 0 ? 'Hombre' : 'Otro'),
        r[2] === 1 ? 'Fines de mercado' : (r[2] === 0 ? 'Autoconsumo' : 'Otra'),
        r[3] === 1 ? 'ATP' : 'NO ATP',
        `"${VOCAB.munis[r[5]]}"`,
        `"${VOCAB.adrs[r[4]]}"`,
        `"${VOCAB.otes[r[12]].replace(/"/g, '""')}"`,
        r[7] || '',
        r[8] || '',
        r[9] === 1 ? 'SI' : 'NO',
        `"${VOCAB.jurs[r[10]]}"`,
        r[11] || 0
      ]);

      const csvContent = "data:text/csv;charset=utf-8,\uFEFF" 
        + [headers.join(','), ...rows.map(e => e.join(','))].join('\\n');

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `censo_agro_bizkaia_filtrado_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  </script>
</body>
</html>
"""

target_filename = "explorador_agro_bizkaia.html"
with open(target_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {target_filename} successfully! Size: {os.path.getsize(target_filename)/1024:.1f} KB")
