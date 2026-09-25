# -*- coding: utf-8 -*-
"""
Script to generate the brand new interactive viewer: visor_mujeres_agro_bizkaia.html
Based on: 20260924_0734_DATOS EXPLOTACIONES DE ALTA_ULTIMA VERSIÓN.xlsx
"""
import openpyxl
import json
import os

print("Building visor_mujeres_agro_bizkaia.html...")

# Load scratch_dataset.json created earlier
with open('scratch_dataset.json', 'r', encoding='utf-8') as f:
    raw_dataset = json.load(f)

print(f"Loaded {len(raw_dataset)} records for the dynamic explorer.")

# Embed the dataset into the HTML generator
dataset_json_str = json.dumps(raw_dataset, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observatorio de las Mujeres en el Sector Agrario de Bizkaia | Bizkaiko Emakume Baserritarren Behatokia</title>
  
  <!-- Google Fonts: Plus Jakarta Sans & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Chart.js 4.4.1 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {
      /* Institutional Green Palette */
      --foral-950: #061911;
      --foral-900: #0A2318;
      --foral-800: #123826;
      --foral-700: #1B4D36;
      --foral-600: #266B4B;
      --foral-500: #10B981;
      --foral-100: #E6F3EC;
      --foral-50:  #F4F9F6;

      /* Professional Segment ATP (Emerald) */
      --atp-primary: #059669;
      --atp-dark: #065F46;
      --atp-light: #ECFDF5;
      --atp-border: #A7F3D0;
      --atp-text: #065F46;
      --atp-shadow: rgba(5, 150, 105, 0.2);

      /* Segment NO ATP (Warm Amber / Ochre) */
      --noatp-primary: #D97706;
      --noatp-dark: #B45309;
      --noatp-light: #FFFBEB;
      --noatp-border: #FDE68A;
      --noatp-text: #92400E;
      --noatp-shadow: rgba(217, 119, 6, 0.2);

      /* Gender Accent (Rose / Terracotta) */
      --mujer-primary: #E11D48;
      --mujer-dark: #BE123C;
      --mujer-light: #FFF1F2;
      --mujer-border: #FECDD3;
      --hombre-primary: #3B82F6;
      --hombre-dark: #1D4ED8;
      --hombre-light: #EFF6FF;

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

      --card-radius: 16px;
      --card-radius-sm: 12px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 4px 20px -2px rgba(15, 23, 42, 0.08);
      --shadow-lg: 0 12px 32px -4px rgba(15, 23, 42, 0.12);
      --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #F8FAF9;
      color: var(--slate-800);
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    h1, h2, h3, h4, h5, .font-heading {
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Top Institutional Header */
    .gov-bar {
      background: var(--foral-950);
      color: #FFFFFF;
      padding: 12px 28px;
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      position: sticky;
      top: 0;
      z-index: 1000;
      backdrop-filter: blur(8px);
    }

    .gov-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }

    .gov-emblem {
      width: 24px;
      height: 24px;
      fill: #10B981;
    }

    .gov-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .lang-btn {
      background: rgba(255, 255, 255, 0.12);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 5px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: var(--transition);
    }

    .lang-btn:hover, .lang-btn.active {
      background: #FFFFFF;
      color: var(--foral-900);
      border-color: #FFFFFF;
    }

    .print-btn {
      background: rgba(255, 255, 255, 0.1);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 5px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
    }

    .print-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    /* Container */
    .container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 24px 80px 24px;
    }

    /* Hero Section */
    .hero-card {
      background: linear-gradient(135deg, #061911 0%, #0F3323 50%, #164E38 100%);
      color: #FFFFFF;
      border-radius: var(--card-radius);
      padding: 40px;
      margin-bottom: 36px;
      box-shadow: 0 16px 40px -8px rgba(6, 25, 17, 0.35);
      position: relative;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hero-card::after {
      content: "";
      position: absolute;
      top: -80px;
      right: -80px;
      width: 320px;
      height: 320px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(8px);
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 16px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #A7F3D0;
    }

    .hero-title {
      font-size: 34px;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 14px;
      letter-spacing: -0.8px;
    }

    .hero-subtitle {
      font-size: 16.5px;
      color: rgba(255, 255, 255, 0.9);
      max-width: 950px;
      line-height: 1.6;
      margin-bottom: 28px;
    }

    .hero-stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      padding-top: 24px;
    }

    .hero-kpi-card {
      background: rgba(255, 255, 255, 0.07);
      backdrop-filter: blur(8px);
      padding: 18px 20px;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      transition: var(--transition);
    }

    .hero-kpi-card:hover {
      background: rgba(255, 255, 255, 0.11);
      transform: translateY(-2px);
    }

    .hero-kpi-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: rgba(255, 255, 255, 0.75);
    }

    .hero-kpi-value {
      font-size: 28px;
      font-weight: 800;
      color: #FFFFFF;
      margin: 6px 0 2px 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .hero-kpi-detail {
      font-size: 12.5px;
      color: rgba(255, 255, 255, 0.85);
    }

    /* SECTION 0: MACRO FUNNEL (THE 3 USER-REQUESTED IMAGES) */
    .funnel-container {
      background: #FFFFFF;
      border-radius: var(--card-radius);
      border: 1px solid var(--slate-200);
      box-shadow: var(--shadow-md);
      padding: 32px;
      margin-bottom: 40px;
    }

    .funnel-header {
      margin-bottom: 28px;
      text-align: center;
      max-width: 860px;
      margin-left: auto;
      margin-right: auto;
    }

    .funnel-tag {
      display: inline-block;
      padding: 4px 12px;
      background: var(--foral-100);
      color: var(--foral-800);
      font-size: 12px;
      font-weight: 700;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }

    .funnel-title {
      font-size: 26px;
      font-weight: 800;
      color: var(--slate-900);
      margin-bottom: 8px;
    }

    .funnel-desc {
      font-size: 15px;
      color: var(--slate-600);
      line-height: 1.5;
    }

    /* Step Nav Tabs */
    .funnel-steps-nav {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 32px;
    }

    .funnel-step-btn {
      background: var(--slate-50);
      border: 2px solid var(--slate-200);
      border-radius: 14px;
      padding: 16px 20px;
      cursor: pointer;
      text-align: left;
      transition: var(--transition);
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .funnel-step-btn:hover {
      border-color: var(--foral-500);
      background: var(--slate-100);
    }

    .funnel-step-btn.active {
      background: #FFFFFF;
      border-color: var(--foral-700);
      box-shadow: 0 4px 14px rgba(27, 77, 54, 0.15);
    }

    .step-number {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--slate-200);
      color: var(--slate-700);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 15px;
      flex-shrink: 0;
      transition: var(--transition);
    }

    .funnel-step-btn.active .step-number {
      background: var(--foral-700);
      color: #FFFFFF;
    }

    .step-info-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--slate-900);
      margin-bottom: 2px;
    }

    .step-info-subtitle {
      font-size: 12px;
      color: var(--slate-500);
    }

    /* Step Content Cards */
    .funnel-step-panel {
      display: none;
      animation: fadeIn 0.3s ease;
    }

    .funnel-step-panel.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .step-visual-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 28px;
      align-items: center;
    }

    .step-chart-box {
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 14px;
      padding: 24px;
      position: relative;
      min-height: 320px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    .step-narrative-box {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .narrative-headline {
      font-size: 20px;
      font-weight: 800;
      color: var(--slate-900);
      line-height: 1.35;
    }

    .narrative-p {
      font-size: 14.5px;
      color: var(--slate-600);
      line-height: 1.6;
    }

    .narrative-metrics {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-top: 4px;
    }

    .metric-pill {
      padding: 14px 16px;
      border-radius: 12px;
      border: 1px solid var(--slate-200);
      background: #FFFFFF;
    }

    .metric-pill.highlight-mujer {
      border-color: var(--mujer-border);
      background: var(--mujer-light);
    }

    .metric-pill.highlight-hombre {
      border-color: var(--slate-300);
      background: var(--slate-100);
    }

    .metric-pill.highlight-atp {
      border-color: var(--atp-border);
      background: var(--atp-light);
    }

    .metric-pill.highlight-noatp {
      border-color: var(--noatp-border);
      background: var(--noatp-light);
    }

    .metric-pill-title {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--slate-500);
      margin-bottom: 4px;
    }

    .metric-pill-val {
      font-size: 22px;
      font-weight: 800;
      color: var(--slate-900);
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .metric-pill-sub {
      font-size: 12px;
      color: var(--slate-600);
      margin-top: 2px;
    }

    .insight-badge {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      background: #FEF3C7;
      border: 1px solid #FCD34D;
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 13px;
      color: #92400E;
      line-height: 1.45;
    }

    .insight-badge svg {
      flex-shrink: 0;
      margin-top: 2px;
    }

    /* CONTROL PANEL (STICKY FILTER & SHORTCUTS) */
    .control-panel {
      position: sticky;
      top: 54px;
      z-index: 900;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border: 1px solid var(--slate-200);
      border-radius: var(--card-radius);
      padding: 14px 20px;
      margin-bottom: 36px;
      box-shadow: var(--shadow-md);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .view-modes {
      display: flex;
      align-items: center;
      background: var(--slate-100);
      padding: 4px;
      border-radius: 12px;
      gap: 4px;
    }

    .view-btn {
      border: none;
      background: transparent;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      color: var(--slate-600);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      user-select: none;
    }

    .view-btn:hover {
      color: var(--slate-900);
    }

    .view-btn.active {
      background: #FFFFFF;
      color: var(--slate-900);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .dot-dual { background: var(--slate-800); }
    .dot-all { background: var(--mujer-primary); }
    .dot-atp { background: var(--atp-primary); }
    .dot-noatp { background: var(--noatp-primary); }

    .nav-chips {
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      max-width: 100%;
      padding-bottom: 2px;
    }

    .nav-chip {
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      color: var(--slate-600);
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      padding: 5px 12px;
      border-radius: 20px;
      white-space: nowrap;
      transition: var(--transition);
    }

    .nav-chip:hover {
      background: var(--slate-200);
      color: var(--slate-900);
      border-color: var(--slate-300);
    }

    /* THEMATIC BLOCKS */
    .block-section {
      margin-bottom: 48px;
      scroll-margin-top: 130px;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 16px;
    }

    .section-tag {
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--foral-700);
      margin-bottom: 4px;
    }

    .section-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--slate-900);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .section-desc {
      font-size: 14.5px;
      color: var(--slate-600);
      max-width: 880px;
      margin-top: 4px;
      line-height: 1.5;
    }

    .section-badges {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
    }

    .badge-atp {
      background: var(--atp-light);
      color: var(--atp-dark);
      border: 1px solid var(--atp-border);
    }

    .badge-noatp {
      background: var(--noatp-light);
      color: var(--noatp-dark);
      border: 1px solid var(--noatp-border);
    }

    .badge-total {
      background: var(--mujer-light);
      color: var(--mujer-dark);
      border: 1px solid var(--mujer-border);
    }

    /* Cards */
    .card {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--card-radius);
      box-shadow: var(--shadow-sm);
      padding: 24px;
      margin-bottom: 20px;
      transition: var(--transition);
    }

    .card:hover {
      box-shadow: var(--shadow-md);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--slate-100);
      padding-bottom: 12px;
    }

    .card-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--slate-900);
    }

    .chart-container-lg {
      position: relative;
      height: 380px;
      width: 100%;
    }

    .chart-container-md {
      position: relative;
      height: 290px;
      width: 100%;
    }

    /* Grid 2 Columns */
    .grid-2col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }

    /* Dual Cards Display */
    .dual-card {
      border-radius: var(--card-radius-sm);
      padding: 20px;
      border: 1px solid var(--slate-200);
      background: #FFFFFF;
    }

    .dual-card.atp {
      border-top: 4px solid var(--atp-primary);
      background: linear-gradient(180deg, rgba(236, 253, 245, 0.4) 0%, #FFFFFF 100%);
    }

    .dual-card.noatp {
      border-top: 4px solid var(--noatp-primary);
      background: linear-gradient(180deg, rgba(255, 251, 235, 0.4) 0%, #FFFFFF 100%);
    }

    .dual-card-title {
      font-size: 15px;
      font-weight: 800;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .dual-card.atp .dual-card-title { color: var(--atp-dark); }
    .dual-card.noatp .dual-card-title { color: var(--noatp-dark); }

    /* Data Highlights & "Data Speaks For Itself" callouts */
    .data-speaks-card {
      background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
      border: 1px solid var(--slate-200);
      border-left: 5px solid var(--foral-700);
      border-radius: var(--card-radius-sm);
      padding: 20px 24px;
      margin-top: 18px;
    }

    .data-speaks-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--foral-700);
      margin-bottom: 6px;
    }

    .data-speaks-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--slate-900);
      margin-bottom: 6px;
    }

    .data-speaks-text {
      font-size: 14px;
      color: var(--slate-700);
      line-height: 1.6;
    }

    /* Table styles */
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 8px;
    }

    .data-table th {
      background: var(--slate-100);
      color: var(--slate-700);
      font-weight: 700;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--slate-200);
    }

    .data-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--slate-100);
      color: var(--slate-800);
    }

    .data-table tr:hover td {
      background: var(--slate-50);
    }

    .progress-bar-wrap {
      width: 100%;
      height: 8px;
      background: var(--slate-100);
      border-radius: 4px;
      overflow: hidden;
      margin-top: 4px;
    }

    .progress-bar-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.6s ease;
    }

    .fill-atp { background: var(--atp-primary); }
    .fill-noatp { background: var(--noatp-primary); }
    .fill-mujer { background: var(--mujer-primary); }

    /* DYNAMIC EXPLORER SECTION */
    .explorer-container {
      background: #FFFFFF;
      border: 1px solid var(--slate-200);
      border-radius: var(--card-radius);
      box-shadow: var(--shadow-md);
      padding: 32px;
      margin-bottom: 48px;
    }

    .filter-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
      background: var(--slate-50);
      padding: 20px;
      border-radius: var(--card-radius-sm);
      border: 1px solid var(--slate-200);
    }

    .filter-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .filter-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--slate-600);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .filter-select {
      padding: 9px 12px;
      border: 1px solid var(--slate-300);
      border-radius: 8px;
      font-size: 13.5px;
      background: #FFFFFF;
      color: var(--slate-800);
      font-family: inherit;
      outline: none;
      cursor: pointer;
      transition: var(--transition);
    }

    .filter-select:focus {
      border-color: var(--foral-600);
      box-shadow: 0 0 0 3px rgba(38, 107, 75, 0.15);
    }

    .explorer-metrics-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }

    .exp-metric-card {
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      padding: 16px;
      border-radius: 12px;
      text-align: center;
    }

    .exp-metric-val {
      font-size: 26px;
      font-weight: 800;
      color: var(--slate-900);
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .exp-metric-lbl {
      font-size: 11.5px;
      color: var(--slate-500);
      font-weight: 700;
      text-transform: uppercase;
      margin-top: 4px;
    }

    .explorer-table-wrap {
      max-height: 400px;
      overflow-y: auto;
      border: 1px solid var(--slate-200);
      border-radius: 10px;
    }

    /* MATRIX SECTION */
    .matrix-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }

    .matrix-card {
      padding: 24px;
      border-radius: 14px;
      border: 1px solid var(--slate-200);
      background: #FFFFFF;
      position: relative;
    }

    .matrix-card.q1 { border-top: 5px solid #EF4444; }
    .matrix-card.q2 { border-top: 5px solid #10B981; }
    .matrix-card.q3 { border-top: 5px solid #3B82F6; }
    .matrix-card.q4 { border-top: 5px solid #8B5CF6; }

    .matrix-tag {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .q1 .matrix-tag { color: #EF4444; }
    .q2 .matrix-tag { color: #10B981; }
    .q3 .matrix-tag { color: #3B82F6; }
    .q4 .matrix-tag { color: #8B5CF6; }

    .matrix-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--slate-900);
      margin-bottom: 10px;
    }

    .matrix-text {
      font-size: 13.5px;
      color: var(--slate-600);
      line-height: 1.5;
    }

    /* Footer */
    footer.gov-footer {
      background: var(--foral-950);
      color: rgba(255, 255, 255, 0.7);
      padding: 40px 24px;
      font-size: 13px;
      margin-top: 60px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer-content {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }

    /* Print Styles */
    @media print {
      .gov-bar, .control-panel, .funnel-steps-nav, .filter-grid {
        display: none !important;
      }
      .container {
        padding: 0;
        max-width: 100%;
      }
      .card, .funnel-container, .explorer-container {
        box-shadow: none !important;
        border: 1px solid #ccc !important;
        page-break-inside: avoid;
      }
      .funnel-step-panel {
        display: block !important;
        margin-bottom: 30px;
      }
    }

    @media (max-width: 1024px) {
      .hero-stats-grid { grid-template-columns: repeat(2, 1fr); }
      .funnel-steps-nav { grid-template-columns: 1fr; }
      .step-visual-grid { grid-template-columns: 1fr; }
      .grid-2col { grid-template-columns: 1fr; }
      .matrix-grid { grid-template-columns: 1fr; }
      .explorer-metrics-row { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 640px) {
      .hero-stats-grid { grid-template-columns: 1fr; }
      .narrative-metrics { grid-template-columns: 1fr; }
      .explorer-metrics-row { grid-template-columns: 1fr; }
    }
  </style>
</head>

<body class="mode-dual">

  <!-- TOP INSTITUTIONAL BAR -->
  <header class="gov-bar">
    <div class="gov-brand">
      <svg class="gov-emblem" viewBox="0 0 24 24">
        <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm1 14.5h-2v-2h2v2zm0-4h-2V7h2v5.5z"/>
      </svg>
      <span id="txt-gov-brand">BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA</span>
    </div>
    <div class="gov-actions">
      <button class="lang-btn active" id="btn-lang-es" onclick="setLang('es')">ES</button>
      <button class="lang-btn" id="btn-lang-eu" onclick="setLang('eu')">EU</button>
      <button class="print-btn" onclick="window.print()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 6 2 18 2 18 9"></polyline>
          <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
          <rect x="6" y="14" width="12" height="8"></rect>
        </svg>
        <span id="txt-print-btn">Imprimir / PDF</span>
      </button>
    </div>
  </header>

  <main class="container">

    <!-- HERO SECTION -->
    <section class="hero-card">
      <div class="hero-badge">
        <span class="dot dot-dual" style="background:#10B981;"></span>
        <span id="txt-hero-badge">OBSERVATORIO DE GÉNERO Y ESTRUCTURA AGRARIA · INFORME FORAL BIZKAIA · AMATERRA</span>
      </div>
      <h1 class="hero-title" id="txt-hero-title">
        Visor Analítico: Las Mujeres en el Sector Agrario de Bizkaia
      </h1>
      <p class="hero-subtitle" id="txt-hero-subtitle">
        Desglose metodológico en 3 fases: desde el censo global (12.120 explotaciones), el filtrado del autoconsumo (3.322 de mercado) y la diferenciación cualitativa entre el segmento profesional <strong>ATP (190 mujeres)</strong> y el colectivo comercial <strong>No ATP (1.004 mujeres)</strong>.
      </p>

      <div class="hero-stats-grid">
        <div class="hero-kpi-card">
          <div class="hero-kpi-label" id="txt-hkpi1-lbl">Censo Total Bizkaia</div>
          <div class="hero-kpi-value">12.120</div>
          <div class="hero-kpi-detail" id="txt-hkpi1-det">3.662 Mujeres (30,2%) | 8.458 Hombres</div>
        </div>
        <div class="hero-kpi-card">
          <div class="hero-kpi-label" id="txt-hkpi2-lbl">Fines de Mercado</div>
          <div class="hero-kpi-value">3.322</div>
          <div class="hero-kpi-detail" id="txt-hkpi2-det">1.194 Mujeres (35,9%) | 2.128 Hombres</div>
        </div>
        <div class="hero-kpi-card" style="border-left: 4px solid var(--atp-primary);">
          <div class="hero-kpi-label" id="txt-hkpi3-lbl">Profesionales (ATP)</div>
          <div class="hero-kpi-value" style="color: #6EE7B7;">190 Mujeres</div>
          <div class="hero-kpi-detail" id="txt-hkpi3-det">35,9% de los 529 ATPs forales</div>
        </div>
        <div class="hero-kpi-card" style="border-left: 4px solid var(--noatp-primary);">
          <div class="hero-kpi-label" id="txt-hkpi4-lbl">Mercado No ATP</div>
          <div class="hero-kpi-value" style="color: #FCD34D;">1.004 Mujeres</div>
          <div class="hero-kpi-detail" id="txt-hkpi4-det">35,9% de los 2.793 No ATP de mercado</div>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- NIVEL 0: EL EMBUDO MACROESTRUCTURAL (LAS 3 IMÁGENES FUNDAMENTALES)        -->
    <!-- ========================================================================= -->
    <section class="funnel-container" id="sec-embudo">
      <div class="funnel-header">
        <span class="funnel-tag" id="txt-funnel-tag">Metodología de Segmentación Foral</span>
        <h2 class="funnel-title" id="txt-funnel-title">Las 3 Imágenes Clave de la Brecha Agraria</h2>
        <p class="funnel-desc" id="txt-funnel-desc">
          Para comprender con exactitud la situación real de las mujeres rurales en Bizkaia, es indispensable aislar el censo residencial o de recreo y descender capa a capa hasta las explotaciones con trascendencia económica.
        </p>
      </div>

      <!-- Step Navigation Buttons -->
      <div class="funnel-steps-nav">
        <button class="funnel-step-btn active" id="btn-step-1" onclick="switchFunnelStep(1)">
          <div class="step-number">1</div>
          <div>
            <div class="step-info-title" id="txt-step1-tab-title">1. Censo Total Bizkaia</div>
            <div class="step-info-subtitle" id="txt-step1-tab-sub">Hombres vs Mujeres en su totalidad</div>
          </div>
        </button>

        <button class="funnel-step-btn" id="btn-step-2" onclick="switchFunnelStep(2)">
          <div class="step-number">2</div>
          <div>
            <div class="step-info-title" id="txt-step2-tab-title">2. Quitando Autoconsumo</div>
            <div class="step-info-subtitle" id="txt-step2-tab-sub">Actividad con Fines de Mercado</div>
          </div>
        </button>

        <button class="funnel-step-btn" id="btn-step-3" onclick="switchFunnelStep(3)">
          <div class="step-number">3</div>
          <div>
            <div class="step-info-title" id="txt-step3-tab-title">3. Separando ATP y No ATP</div>
            <div class="step-info-subtitle" id="txt-step3-tab-sub">Profesionales vs Complementarias</div>
          </div>
        </button>
      </div>

      <!-- STEP 1 PANEL: CENSO TOTAL -->
      <div class="funnel-step-panel active" id="panel-step-1">
        <div class="step-visual-grid">
          <div class="step-chart-box">
            <h4 style="font-size:14px; font-weight:700; color:var(--slate-700); margin-bottom:12px;" id="txt-step1-chart-title">
              Distribución por Sexo del Censo Agrario Total (12.120 Explotaciones)
            </h4>
            <div style="width: 250px; height: 250px; position: relative;">
              <canvas id="chartFunnelStep1"></canvas>
            </div>
          </div>
          <div class="step-narrative-box">
            <h3 class="narrative-headline" id="txt-step1-head">
              Primera Imagen: 3 de cada 10 explotaciones registradas en Bizkaia están a nombre de una mujer
            </h3>
            <p class="narrative-p" id="txt-step1-p">
              El censo agrario oficial de la Diputación Foral de Bizkaia contabiliza <strong>12.120 explotaciones</strong> (excluyendo registros institucionales o asociaciones). De ellas, <strong>8.458 son ostentadas por hombres (69,8%)</strong> y <strong>3.662 por mujeres (30,2%)</strong>.
            </p>
            <div class="narrative-metrics">
              <div class="metric-pill highlight-hombre">
                <div class="metric-pill-title" id="txt-step1-m1-lbl">Hombres (Censo Total)</div>
                <div class="metric-pill-val">8.458</div>
                <div class="metric-pill-sub">69,79% de los titulares forales</div>
              </div>
              <div class="metric-pill highlight-mujer">
                <div class="metric-pill-title" id="txt-step1-m2-lbl">Mujeres (Censo Total)</div>
                <div class="metric-pill-val">3.662</div>
                <div class="metric-pill-sub">30,21% de las titulares forales</div>
              </div>
            </div>
            <div class="insight-badge">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div id="txt-step1-insight">
                <strong>Clave de lectura:</strong> Esta cifra macro engloba tanto las grandes ganaderías como los pequeños huertos domésticos de fin de semana. No refleja todavía la economía productiva real.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 2 PANEL: QUITANDO AUTOCONSUMO -->
      <div class="funnel-step-panel" id="panel-step-2">
        <div class="step-visual-grid">
          <div class="step-chart-box">
            <h4 style="font-size:14px; font-weight:700; color:var(--slate-700); margin-bottom:12px;" id="txt-step2-chart-title">
              Censo Total Filtrado: Autoconsumo (8.798) vs Fines de Mercado (3.322)
            </h4>
            <div style="width: 100%; height: 260px; position: relative;">
              <canvas id="chartFunnelStep2"></canvas>
            </div>
          </div>
          <div class="step-narrative-box">
            <h3 class="narrative-headline" id="txt-step2-head">
              Segunda Imagen: Al eliminar el autoconsumo, la cuota femenina sube casi 6 puntos porcentuales
            </h3>
            <p class="narrative-p" id="txt-step2-p">
              El <strong>72,6% de todo el censo foral (8.798 explotaciones)</strong> son de mero autoconsumo o recreo doméstico. Al retirar este estrato no comercial, el campo bizkaíno real queda configurado por <strong>3.322 explotaciones con fines de mercado</strong>: 2.128 hombres (64,1%) y <strong>1.194 mujeres (35,9%)</strong>.
            </p>
            <div class="narrative-metrics">
              <div class="metric-pill" style="border-color: #94A3B8; background:#F8FAFC;">
                <div class="metric-pill-title" id="txt-step2-m1-lbl">Autoconsumo Doméstico</div>
                <div class="metric-pill-val">8.798</div>
                <div class="metric-pill-sub">72,59% del censo (2.468 mujeres)</div>
              </div>
              <div class="metric-pill highlight-mujer">
                <div class="metric-pill-title" id="txt-step2-m2-lbl">Fines de Mercado</div>
                <div class="metric-pill-val">3.322</div>
                <div class="metric-pill-sub"><strong>1.194 mujeres (35,94%)</strong></div>
              </div>
            </div>
            <div class="insight-badge" style="background:#ECFDF5; border-color:#A7F3D0; color:#065F46;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <div id="txt-step2-insight">
                <strong>El dato habla por sí solo:</strong> Cuando se mide actividad comercial efectiva, la presencia de mujeres no mengua, sino que <strong>se incrementa del 30,2% al 35,9%</strong> (+5,7%). Las mujeres representan una fuerza tractora decisiva en las explotaciones mercantiles.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 3 PANEL: SEPARANDO ATP Y NO ATP -->
      <div class="funnel-step-panel" id="panel-step-3">
        <div class="step-visual-grid">
          <div class="step-chart-box">
            <h4 style="font-size:14px; font-weight:700; color:var(--slate-700); margin-bottom:12px;" id="txt-step3-chart-title">
              Segmentación de Mercado: Profesionales ATP (529) vs No ATP (2.793)
            </h4>
            <div style="width: 100%; height: 260px; position: relative;">
              <canvas id="chartFunnelStep3"></canvas>
            </div>
          </div>
          <div class="step-narrative-box">
            <h3 class="narrative-headline" id="txt-step3-head">
              Tercera Imagen: Separando el universo profesional ATP del colectivo No ATP
            </h3>
            <p class="narrative-p" id="txt-step3-p">
              Dentro de las 3.322 explotaciones de mercado se produce la división crucial de profesionalización:
              <strong>529 explotaciones ATP</strong> (donde la titular cotiza a la Seguridad Social agraria y obtiene más del 50% de su renta y tiempo de trabajo) frente a <strong>2.793 explotaciones No ATP</strong> (actividad agraria comercial a tiempo parcial, complementaria o de titulares jubiladas).
            </p>
            <div class="narrative-metrics">
              <div class="metric-pill highlight-atp">
                <div class="metric-pill-title" id="txt-step3-m1-lbl">Mujeres ATP (Profesionales)</div>
                <div class="metric-pill-val" style="color:var(--atp-dark);">190</div>
                <div class="metric-pill-sub"><strong>35,92%</strong> de las 529 ATPs forales</div>
              </div>
              <div class="metric-pill highlight-noatp">
                <div class="metric-pill-title" id="txt-step3-m2-lbl">Mujeres No ATP (Mercado)</div>
                <div class="metric-pill-val" style="color:var(--noatp-dark);">1.004</div>
                <div class="metric-pill-sub"><strong>35,95%</strong> de los 2.793 No ATP forales</div>
              </div>
            </div>
            <div class="insight-badge" style="background:#FFFBEB; border-color:#FDE68A; color:#92400E;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              <div id="txt-step3-insight">
                <strong>La Paradoja de la Paridad Porcentual:</strong> En ambos colectivos las mujeres representan con exactitud milimétrica el <strong>35,9%</strong>. Sin embargo, su realidad productiva, edad, superficie y capacidad de relevo son mundos completamente antagónicos, como revelan los cuadros siguientes.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- STICKY CONTROL PANEL: VISOR SWITCHER & SHORTCUT NAVIGATION               -->
    <!-- ========================================================================= -->
    <nav class="control-panel">
      <div class="view-modes">
        <button class="view-btn mode-dual active" id="btn-view-dual" onclick="setViewMode('dual')">
          <span class="dot dot-dual"></span>
          <span id="txt-view-dual">Comparativa Dual (Lado a Lado)</span>
        </button>
        <button class="view-btn mode-all" id="btn-view-all" onclick="setViewMode('all')">
          <span class="dot dot-all"></span>
          <span id="txt-view-all">Total Mujeres Mercado (1.194)</span>
        </button>
        <button class="view-btn mode-atp" id="btn-view-atp" onclick="setViewMode('atp')">
          <span class="dot dot-atp"></span>
          <span id="txt-view-atp">Solo ATP (190)</span>
        </button>
        <button class="view-btn mode-noatp" id="btn-view-noatp" onclick="setViewMode('noatp')">
          <span class="dot dot-noatp"></span>
          <span id="txt-view-noatp">Solo NO ATP (1.004)</span>
        </button>
      </div>

      <div class="nav-chips">
        <a href="#bloque-subsectores" class="nav-chip" id="chip-1">1. Subsectores</a>
        <a href="#bloque-superficie" class="nav-chip" id="chip-2">2. Superficie</a>
        <a href="#bloque-ecologico" class="nav-chip" id="chip-3">3. Ecológico</a>
        <a href="#bloque-comarcas" class="nav-chip" id="chip-4">4. Comarcas</a>
        <a href="#bloque-juridica" class="nav-chip" id="chip-5">5. Forma Jurídica</a>
        <a href="#bloque-edad" class="nav-chip" id="chip-6">6. Edad y Relevo</a>
        <a href="#bloque-utas" class="nav-chip" id="chip-7">7. Trabajo (UTAs)</a>
        <a href="#bloque-municipios" class="nav-chip" id="chip-8">8. Top Municipios</a>
        <a href="#bloque-matriz" class="nav-chip" id="chip-9">9. Matriz Estratégica</a>
        <a href="#bloque-explorador" class="nav-chip" id="chip-10" style="background:#10B981; color:#fff; font-weight:700;">★ 10. Explorador en Vivo</a>
      </div>
    </nav>

    <!-- ========================================================================= -->
    <!-- BLOQUE 1: SUBSECTORES PRODUCTIVOS (OTE)                                   -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-subsectores">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec1-tag">INDICADOR ESTRUCTURAL 1</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>
            </svg>
            <span id="txt-sec1-title">Orientación Productiva y Subsectores</span>
          </h2>
          <p class="section-desc" id="txt-sec1-desc">
            Distribución de las 1.194 mujeres con fines de mercado según su Clasificación Técnico-Económica (OTE). Contraste directo de especialización entre el núcleo profesional ATP (190) y el colectivo No ATP (1.004).
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title" id="txt-sec1-ctitle">Especialización Productiva (% de Mujeres en cada colectivo)</div>
          <span class="badge" style="background:var(--slate-100); color:var(--slate-700);">Top 8 Subsectores</span>
        </div>
        <div class="chart-container-lg">
          <canvas id="chartSubsectores"></canvas>
        </div>
      </div>

      <!-- Dual Breakdown Cards -->
      <div class="grid-2col">
        <div class="dual-card atp" id="card-sub-atp">
          <div class="dual-card-title">
            <span>Mujeres Profesionales ATP (190)</span>
            <span class="badge badge-atp">100% Profesionales</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Subsector OTE</th><th>Mujeres</th><th>% ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Bovinos cría y carne</td><td><strong>83</strong></td><td>43,7%</td></tr>
              <tr><td>Bovinos leche</td><td><strong>25</strong></td><td>13,2%</td></tr>
              <tr><td>Hortalizas en invernadero</td><td><strong>17</strong></td><td>8,9%</td></tr>
              <tr><td>Aves ponedoras</td><td><strong>11</strong></td><td>5,8%</td></tr>
              <tr><td>Ovinos carne y leche</td><td><strong>9</strong></td><td>4,7%</td></tr>
              <tr><td>Hortalizas al aire libre</td><td><strong>9</strong></td><td>4,7%</td></tr>
              <tr><td>Fruticultura</td><td><strong>9</strong></td><td>4,7%</td></tr>
              <tr><td>Viticultura (Txakoli)</td><td><strong>7</strong></td><td>3,7%</td></tr>
              <tr><td>Otras / No clasificadas</td><td><strong>20</strong></td><td>10,5%</td></tr>
            </tbody>
          </table>
        </div>

        <div class="dual-card noatp" id="card-sub-noatp">
          <div class="dual-card-title">
            <span>Mujeres Comerciales NO ATP (1.004)</span>
            <span class="badge badge-noatp">Complementarias</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Subsector OTE</th><th>Mujeres</th><th>% No ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Bovinos cría y carne</td><td><strong>448</strong></td><td>44,6%</td></tr>
              <tr><td>Ovinos especializados</td><td><strong>122</strong></td><td>12,2%</td></tr>
              <tr><td>No clasificadas / mixtas</td><td><strong>104</strong></td><td>10,4%</td></tr>
              <tr><td>Hortalizas al aire libre</td><td><strong>78</strong></td><td>7,8%</td></tr>
              <tr><td>Hortalizas en invernadero</td><td><strong>60</strong></td><td>6,0%</td></tr>
              <tr><td>Fruticultura especializada</td><td><strong>58</strong></td><td>5,8%</td></tr>
              <tr><td>Viticultura (Txakoli)</td><td><strong>36</strong></td><td>3,6%</td></tr>
              <tr><td>Herbívoros varios</td><td><strong>33</strong></td><td>3,3%</td></tr>
              <tr><td>Bovinos leche</td><td><strong>10</strong></td><td>1,0%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Data Speaks Callout -->
      <div class="data-speaks-card">
        <div class="data-speaks-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec1-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec1-insight-title">
          La Leche es 13 Veces más Exclusiva de las Profesionales; el Ovino es el Refugio Tradicional No ATP
        </div>
        <div class="data-speaks-text" id="txt-sec1-insight-text">
          Mientras que el vacuno de carne es el eje vertebrador común (44% en ambos grupos), el <strong>vacuno de leche exige dedicación a tiempo completo</strong>: el 13,2% de las mujeres ATP se dedican a leche (25 titulares), frente a un testimonial 1,0% en No ATP (10 titulares). Por el contrario, el <strong>ovino tradicional</strong> quintuplica su peso relativo en No ATP (12,2% con 122 pastoras) respecto a las profesionales ATP (4,7% con 9 pastoras). Asimismo, la avicultura de puesta tecnificada es un nicho típicamente profesional (5,8% en ATP vs 0,8% en No ATP).
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 2: SUPERFICIE Y CONCENTRACIÓN DE TIERRA                            -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-superficie">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec2-tag">INDICADOR ESTRUCTURAL 2</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>
            </svg>
            <span id="txt-sec2-title">Superficie Agraria y Brecha de Escala</span>
          </h2>
          <p class="section-desc" id="txt-sec2-desc">
            Dimensión física de las explotaciones gestionadas por mujeres en Bizkaia. Distribución porcentual en los cuatro estratos de superficie foral.
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title" id="txt-sec2-ctitle">Distribución de Superficie por Estratos (% dentro de cada colectivo)</div>
          <span class="badge" style="background:var(--slate-100); color:var(--slate-700);">Estratos Forales</span>
        </div>
        <div class="chart-container-lg">
          <canvas id="chartSuperficie"></canvas>
        </div>
      </div>

      <div class="grid-2col">
        <div class="dual-card atp" id="card-sup-atp">
          <div class="dual-card-title">
            <span>Mujeres ATP (190)</span>
            <span class="badge badge-atp">Escala Equilibrada</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Estrato de Superficie</th><th>Titulares</th><th>% Mujeres ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Muy pequeña (0,5 - 5 ha)</td><td><strong>61</strong></td><td>32,1%</td></tr>
              <tr><td>Pequeña (5 - 20 ha)</td><td><strong>52</strong></td><td>27,4%</td></tr>
              <tr><td>Mediana (20 - 50 ha)</td><td><strong>50</strong></td><td>26,3%</td></tr>
              <tr><td>Grande (> 50 ha)</td><td><strong>27</strong></td><td>14,2%</td></tr>
            </tbody>
          </table>
        </div>

        <div class="dual-card noatp" id="card-sup-noatp">
          <div class="dual-card-title">
            <span>Mujeres NO ATP (1.004)</span>
            <span class="badge badge-noatp">Minifundio Extremo</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Estrato de Superficie</th><th>Titulares</th><th>% Mujeres No ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Muy pequeña (0,5 - 5 ha)</td><td><strong>749</strong></td><td>74,6%</td></tr>
              <tr><td>Pequeña (5 - 20 ha)</td><td><strong>199</strong></td><td>19,8%</td></tr>
              <tr><td>Mediana (20 - 50 ha)</td><td><strong>50</strong></td><td>5,0%</td></tr>
              <tr><td>Grande (> 50 ha)</td><td><strong>6</strong></td><td>0,6%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="data-speaks-card">
        <div class="data-speaks-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec2-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec2-insight-title">
          3 de cada 4 Mujeres No ATP Están Confinadas en Menos de 5 Hectáreas
        </div>
        <div class="data-speaks-text" id="txt-sec2-insight-text">
          El <strong>74,6% de las mujeres No ATP comerciales (749 titulares)</strong> disponen de minifundios inferiores a 5 ha, y sólo el 5,6% gestiona más de 20 ha. Por el contrario, en las mujeres profesionales ATP, el <strong>40,5% gestiona medianas o grandes explotaciones (>20 ha)</strong>. Sin acceso a suficiente base territorial, la viabilidad económica plena de las titulares No ATP se vuelve inviable, condicionando su perpetuación como actividad auxiliar o de subsistencia.
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 3: PRODUCCIÓN ECOLÓGICA                                            -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-ecologico">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec3-tag">INDICADOR ESTRUCTURAL 3</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M12 2a9 9 0 0 0-9 9c0 4.97 4.03 9 9 9 4.97 0 9-4.03 9-9 0-4.97-4.03-9-9-9z"/><path d="M12 12m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"/>
            </svg>
            <span id="txt-sec3-title">Producción Ecológica y Sostenibilidad</span>
          </h2>
          <p class="section-desc" id="txt-sec3-desc">
            Nivel de certificación agroecológica oficial de las explotaciones comerciales lideradas por mujeres en Bizkaia.
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <div class="card-title" id="txt-sec3-c1title">Tasa de Adopción Ecológica (% sobre cada colectivo)</div>
          </div>
          <div class="chart-container-md">
            <canvas id="chartEcoRate"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title" id="txt-sec3-c2title">Presencia Femenina en el Total Ecológico de Bizkaia</div>
          </div>
          <div class="chart-container-md">
            <canvas id="chartEcoGenderShare"></canvas>
          </div>
        </div>
      </div>

      <div class="data-speaks-card">
        <div class="data-speaks-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec3-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec3-insight-title">
          Las Mujeres ATP Multiplican por 6,5 la Tasa Ecológica y Aportan el 41% de todo el Eco Profesional
        </div>
        <div class="data-speaks-text" id="txt-sec3-insight-text">
          La vocación ecológica es intensamente profesional: el <strong>11,6% de las mujeres ATP (22 explotaciones)</strong> producen en ecológico, frente a sólo el <strong>1,8% de las mujeres No ATP (18 explotaciones)</strong>. Aún más relevante: en todo Bizkaia sólo hay 54 explotaciones profesionales ATP registradas en ecológico, y de ellas, <strong>22 están regentadas por mujeres (40,74%)</strong>. Las mujeres profesionales constituyen la vanguardia real de la transición verde del modelo agrario foral.
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 4: DISTRIBUCIÓN COMARCAL (ADR)                                     -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-comarcas">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec4-tag">INDICADOR ESTRUCTURAL 4</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            <span id="txt-sec4-title">Distribución Territorial por Comarcas (ADR)</span>
          </h2>
          <p class="section-desc" id="txt-sec4-desc">
            Localización geográfica de las titulares según las 6 Asociaciones de Desarrollo Rural (ADR) de Bizkaia.
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title" id="txt-sec4-ctitle">Peso de Cada Comarca en el Total de Mujeres de su Segmento (%)</div>
          <span class="badge" style="background:var(--slate-100); color:var(--slate-700);">6 Comarcas Forales</span>
        </div>
        <div class="chart-container-lg">
          <canvas id="chartComarcas"></canvas>
        </div>
      </div>

      <div class="grid-2col">
        <div class="dual-card atp" id="card-com-atp">
          <div class="dual-card-title">
            <span>Mujeres ATP por Comarca (190)</span>
            <span class="badge badge-atp">Enkarterri Lidera</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Comarca (ADR)</th><th>Titulares</th><th>% Mujeres ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Enkarterrialde</td><td><strong>78</strong></td><td>41,1%</td></tr>
              <tr><td>Jata Ondo (Uribe)</td><td><strong>31</strong></td><td>16,3%</td></tr>
              <tr><td>Gorbeialde</td><td><strong>29</strong></td><td>15,3%</td></tr>
              <tr><td>Urremendi (Busturialdea)</td><td><strong>20</strong></td><td>10,5%</td></tr>
              <tr><td>Urkiola (Durangaldea)</td><td><strong>19</strong></td><td>10,0%</td></tr>
              <tr><td>Lea-Artibai</td><td><strong>13</strong></td><td>6,8%</td></tr>
            </tbody>
          </table>
        </div>

        <div class="dual-card noatp" id="card-com-noatp">
          <div class="dual-card-title">
            <span>Mujeres NO ATP por Comarca (1.004)</span>
            <span class="badge badge-noatp">Jata Ondo y Enkarterri</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Comarca (ADR)</th><th>Titulares</th><th>% Mujeres No ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Jata Ondo (Uribe)</td><td><strong>261</strong></td><td>26,0%</td></tr>
              <tr><td>Enkarterrialde</td><td><strong>209</strong></td><td>20,8%</td></tr>
              <tr><td>Gorbeialde</td><td><strong>146</strong></td><td>14,5%</td></tr>
              <tr><td>Urremendi (Busturialdea)</td><td><strong>146</strong></td><td>14,5%</td></tr>
              <tr><td>Lea-Artibai</td><td><strong>129</strong></td><td>12,9%</td></tr>
              <tr><td>Urkiola (Durangaldea)</td><td><strong>113</strong></td><td>11,3%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="data-speaks-card">
        <div class="data-speaks-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec4-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec4-insight-title">
          Enkarterri Concentra Más del 41% de todo el Agro Profesional Femenino de Bizkaia
        </div>
        <div class="data-speaks-text" id="txt-sec4-insight-text">
          La comarca de las Encartaciones es el corazón indiscutible de la profesionalización femenina: <strong>78 de las 190 mujeres ATP de Bizkaia (41,1%) radican en Enkarterrialde</strong>, traccionadas por la potencia ganadera de Karrantza, Orduña y Güeñes. En contraste, en el colectivo No ATP, <strong>Jata Ondo (Uribe) ocupa el primer puesto con 261 titulares (26,0%)</strong>, reflejando una estructura periurbana y costera intensiva en huerta y ganadería de escala familiar.
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 5: FORMA JURÍDICA Y TITULARIDAD COMPARTIDA                         -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-juridica">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec5-tag">INDICADOR ESTRUCTURAL 5</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/>
            </svg>
            <span id="txt-sec5-title">Estructura Jurídica y Titularidad Compartida</span>
          </h2>
          <p class="section-desc" id="txt-sec5-desc">
            Forma de personificación mercantil y grado de asociacionismo societario entre las mujeres con explotaciones de mercado.
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: 190 Mujeres</span>
          <span class="badge badge-noatp">NO ATP: 1.004 Mujeres</span>
        </div>
      </div>

      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <div class="card-title" id="txt-sec5-c1title">Distribución Jurídica en Mujeres ATP (190)</div>
          </div>
          <div class="chart-container-md">
            <canvas id="chartJuridicaATP"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title" id="txt-sec5-c2title">Distribución Jurídica en Mujeres NO ATP (1.004)</div>
          </div>
          <div class="chart-container-md">
            <canvas id="chartJuridicaNoATP"></canvas>
          </div>
        </div>
      </div>

      <div class="data-speaks-card" style="border-left-color: #DC2626;">
        <div class="data-speaks-header" style="color: #DC2626;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec5-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec5-insight-title">
          El Espejismo de la Titularidad Compartida: Sólo 3 Mujeres en Toda Bizkaia
        </div>
        <div class="data-speaks-text" id="txt-sec5-insight-text">
          La inmensa mayoría de las mujeres operan en solitario como <strong>persona física (95,2% en No ATP y 80,0% en ATP)</strong>. En el colectivo ATP, un 20% de las profesionales se han dotado de estructuras societarias (Comunidades de Bienes 9,5%, Sociedades Civiles 6,3%, SL 1,6%, Cooperativas 1,1%). No obstante, el dato institucional más demoledor es que <strong>únicamente 3 mujeres en toda Bizkaia están registradas bajo la Ley 35/2011 de Titularidad Compartida</strong> (1,58% de las ATP y 0% en No ATP). Esta figura legal no ha conseguido visibilizar ni formalizar jurídicamente a las cónyuges copropietarias en el territorio.
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 6: EDAD, ENVEJECIMIENTO Y RELEVO GENERACIONAL                       -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-edad">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec6-tag">INDICADOR ESTRUCTURAL 6</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
            </svg>
            <span id="txt-sec6-title">Edad, Envejecimiento y el Abismo del Relevo</span>
          </h2>
          <p class="section-desc" id="txt-sec6-desc">
            Estructura piramidal por edades de las titulares de explotaciones de mercado en Bizkaia.
          </p>
        </div>
        <div class="section-badges">
          <span class="badge badge-atp">ATP: Media 53 años</span>
          <span class="badge badge-noatp">NO ATP: Media 66 años</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title" id="txt-sec6-ctitle">Pirámide Generacional: ATP vs NO ATP (% dentro de cada segmento)</div>
          <span class="badge" style="background:var(--slate-100); color:var(--slate-700);">Tramos de Edad</span>
        </div>
        <div class="chart-container-lg">
          <canvas id="chartEdad"></canvas>
        </div>
      </div>

      <div class="grid-2col">
        <div class="dual-card atp" id="card-edad-atp">
          <div class="dual-card-title">
            <span>Mujeres ATP (190)</span>
            <span class="badge badge-atp">Edad Media: 53 años</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Tramo de Edad</th><th>Titulares</th><th>% Mujeres ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Jóvenes (18 - 40 años)</td><td><strong>33</strong></td><td>17,4%</td></tr>
              <tr><td>Edad Madura (41 - 65 años)</td><td><strong>131</strong></td><td>68,9%</td></tr>
              <tr><td>Jubilación (> 65 años)</td><td><strong>26</strong></td><td>13,7%</td></tr>
            </tbody>
          </table>
        </div>

        <div class="dual-card noatp" id="card-edad-noatp">
          <div class="dual-card-title">
            <span>Mujeres NO ATP (1.004)</span>
            <span class="badge badge-noatp">Edad Media: 66 años</span>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Tramo de Edad</th><th>Titulares</th><th>% Mujeres No ATP</th></tr>
            </thead>
            <tbody>
              <tr><td>Jóvenes (18 - 40 años)</td><td><strong>52</strong></td><td>5,2%</td></tr>
              <tr><td>Edad Madura (41 - 65 años)</td><td><strong>425</strong></td><td>42,3%</td></tr>
              <tr><td>Jubilación (> 65 años)</td><td><strong>527</strong></td><td>52,5%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="data-speaks-card" style="border-left-color: #EF4444;">
        <div class="data-speaks-header" style="color: #EF4444;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
          <span id="txt-sec6-insight-tag">El Dato que Habla por Sí Solo</span>
        </div>
        <div class="data-speaks-title" id="txt-sec6-insight-title">
          Más de la Mitad de las Mujeres No ATP ya Superan la Edad de Jubilación (52,5%)
        </div>
        <div class="data-speaks-text" id="txt-sec6-insight-text">
          La brecha demográfica entre ambos colectivos es abismal: las mujeres No ATP presentan una <strong>edad media de 66 años</strong> y más de la mitad (<strong>527 mujeres, 52,5%</strong>) superan los 65 años, manteniendo la titularidad de explotaciones comerciales aun estando jubiladas, con un recambio juvenil casi nulo (sólo 52 mujeres jóvenes menores de 40 años, 5,2%). Por su parte, el colectivo ATP cuenta con una <strong>edad media de 53 años</strong> y una tasa de mujeres jóvenes del 17,4% (33 titulares). En todo Bizkaia <strong>sólo existen 85 mujeres menores de 40 años</strong> al frente de una explotación con fines de mercado.
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 7: TRABAJO Y VIABILIDAD (UTAs)                                      -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-utas">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec7-tag">NUEVO VISOR 7 · CARGA LABORAL</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M20 7h-7"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>
            </svg>
            <span id="txt-sec7-title">Intensidad Laboral y Empleo Agrario (UTAs)</span>
          </h2>
          <p class="section-desc" id="txt-sec7-desc">
            Unidades de Trabajo Agrario (UTAs): estimación del volumen de mano de obra anual a tiempo completo empleada en las explotaciones de mujeres.
          </p>
        </div>
      </div>

      <div class="grid-2col">
        <div class="card" style="text-align:center; padding:32px;">
          <div style="font-size:13px; font-weight:700; color:var(--atp-dark); text-transform:uppercase;">Mujeres ATP (Profesionales)</div>
          <div style="font-size:48px; font-weight:900; color:var(--atp-primary); margin:12px 0;">1,42 UTAs</div>
          <div style="font-size:14px; color:var(--slate-600); max-width:380px; margin:0 auto;">
            Mano de obra equivalente a <strong>más de 1 jornada completa por explotación</strong>. En muchas ganaderías de leche y huertas intensivas, emplean mano de obra adicional familiar o asalariada.
          </div>
        </div>

        <div class="card" style="text-align:center; padding:32px;">
          <div style="font-size:13px; font-weight:700; color:var(--noatp-dark); text-transform:uppercase;">Mujeres NO ATP (Comerciales)</div>
          <div style="font-size:48px; font-weight:900; color:var(--noatp-primary); margin:12px 0;">0,30 UTAs</div>
          <div style="font-size:14px; color:var(--slate-600); max-width:380px; margin:0 auto;">
            Mano de obra equivalente a <strong>menos de un tercio de jornada (part-time)</strong>. Característico de actividad pluriactiva, ganadería extensiva de bajo laboreo o titulares pensionistas.
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 8: TOP 15 MUNICIPIOS DEL AGRO FEMENINO                            -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-municipios">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec8-tag">NUEVO VISOR 8 · MAPA MUNICIPAL</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>
            </svg>
            <span id="txt-sec8-title">Top 15 Municipios con Mayor Presencia Femenina</span>
          </h2>
          <p class="section-desc" id="txt-sec8-desc">
            Concentración de las 1.194 titulares en los 15 municipios con más explotaciones comerciales de Bizkaia.
          </p>
        </div>
      </div>

      <div class="card">
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Municipio</th>
              <th>Comarca</th>
              <th>Total Mujeres</th>
              <th>Mujeres ATP</th>
              <th>Mujeres No ATP</th>
              <th style="width:25%;">Distribución Gráfica</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1</td><td><strong>Karrantza Harana / Valle de Carranza</strong></td><td>Enkarterrialde</td><td><strong>111</strong></td><td>38</td><td>73</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:100%;"></div></div></td></tr>
            <tr><td>2</td><td><strong>Orozko</strong></td><td>Gorbeialde</td><td><strong>38</strong></td><td>6</td><td>32</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:34%;"></div></div></td></tr>
            <tr><td>3</td><td><strong>Muxika</strong></td><td>Urremendi</td><td><strong>34</strong></td><td>4</td><td>30</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:31%;"></div></div></td></tr>
            <tr><td>4</td><td><strong>Markina-Xemein</strong></td><td>Lea-Artibai</td><td><strong>31</strong></td><td>5</td><td>26</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:28%;"></div></div></td></tr>
            <tr><td>5</td><td><strong>Elorrio</strong></td><td>Urkiola</td><td><strong>27</strong></td><td>3</td><td>24</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:24%;"></div></div></td></tr>
            <tr><td>6</td><td><strong>Mungia</strong></td><td>Jata Ondo</td><td><strong>27</strong></td><td>2</td><td>25</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:24%;"></div></div></td></tr>
            <tr><td>7</td><td><strong>Gatika</strong></td><td>Jata Ondo</td><td><strong>26</strong></td><td>6</td><td>20</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:23%;"></div></div></td></tr>
            <tr><td>8</td><td><strong>Gamiz-Fika</strong></td><td>Jata Ondo</td><td><strong>26</strong></td><td>2</td><td>24</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:23%;"></div></div></td></tr>
            <tr><td>9</td><td><strong>Abadiño</strong></td><td>Urkiola</td><td><strong>25</strong></td><td>3</td><td>22</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:22%;"></div></div></td></tr>
            <tr><td>10</td><td><strong>Mallabia</strong></td><td>Urkiola</td><td><strong>25</strong></td><td>1</td><td>24</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:22%;"></div></div></td></tr>
            <tr><td>11</td><td><strong>Urduña / Orduña</strong></td><td>Enkarterrialde</td><td><strong>24</strong></td><td>7</td><td>17</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:22%;"></div></div></td></tr>
            <tr><td>12</td><td><strong>Zeanuri</strong></td><td>Gorbeialde</td><td><strong>23</strong></td><td>3</td><td>20</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:21%;"></div></div></td></tr>
            <tr><td>13</td><td><strong>Gordexola</strong></td><td>Enkarterrialde</td><td><strong>22</strong></td><td>5</td><td>17</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:20%;"></div></div></td></tr>
            <tr><td>14</td><td><strong>Güeñes</strong></td><td>Enkarterrialde</td><td><strong>22</strong></td><td>5</td><td>17</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:20%;"></div></div></td></tr>
            <tr><td>15</td><td><strong>Bermeo</strong></td><td>Urremendi</td><td><strong>18</strong></td><td>6</td><td>12</td><td><div class="progress-bar-wrap"><div class="progress-bar-fill fill-mujer" style="width:16%;"></div></div></td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 9: MATRIZ DE PRIORIZACIÓN DE POLÍTICAS PÚBLICAS                    -->
    <!-- ========================================================================= -->
    <section class="block-section" id="bloque-matriz">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec9-tag">NUEVO VISOR 9 · ESTRATEGIA FORAL</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span id="txt-sec9-title">Matriz Estratégica: Dónde Actuar Según los Datos</span>
          </h2>
          <p class="section-desc" id="txt-sec9-desc">
            Cuatro cuadrantes de intervención pública foral derivados del análisis cruzado de datos.
          </p>
        </div>
      </div>

      <div class="matrix-grid">
        <div class="matrix-card q1">
          <div class="matrix-tag">Cuadrante Rojo · Urgencia Máxima</div>
          <h3 class="matrix-title">1. Plan de Choque de Relevo en Ganadería Extensiva</h3>
          <p class="matrix-text">
            527 mujeres No ATP tienen más de 65 años (principalmente en vacuno y ovino). Sin un plan foral de transmisión y banco de tierras ágil en Enkarterri, Gorbeialde y Urkiola, cientos de explotaciones se cerrarán de forma definitiva en los próximos 5 años.
          </p>
        </div>

        <div class="matrix-card q2">
          <div class="matrix-tag">Cuadrante Verde · Motor de Futuro</div>
          <h3 class="matrix-title">2. Consolidación de la Vanguardia Agroecológica Femenina</h3>
          <p class="matrix-text">
            Las 22 mujeres ATP ecológicas ya representan el 41% de todo el sector ecológico profesional de Bizkaia. Fomentar canales cortos de comercialización y líneas de inversión específicas para huerta protegida e innovación láctea en estas productoras.
          </p>
        </div>

        <div class="matrix-card q3">
          <div class="matrix-tag">Cuadrante Azul · Potencial de Crecimiento</div>
          <h3 class="matrix-title">3. Pasarela de Profesionalización No ATP → ATP</h3>
          <p class="matrix-text">
            Existen 199 mujeres No ATP con explotaciones de entre 5 y 20 hectáreas con potencial de viabilidad. Un programa de asesoramiento integral de la Diputación podría acompañar la transición hacia la dedicación profesional ATP a aquellas titulares menores de 50 años.
          </p>
        </div>

        <div class="matrix-card q4">
          <div class="matrix-tag">Cuadrante Morado · Reforma Institucional</div>
          <h3 class="matrix-title">4. Superación del Espejismo de la Titularidad Compartida</h3>
          <p class="matrix-text">
            Con sólo 3 casos reales en Bizkaia, es urgente crear incentivos fiscales forales y bonificaciones directas en el IRPF foral para que las comunidades de bienes familiares y matrimonios agrarios formalicen la cotitularidad real de las mujeres en los cuadernos de explotación.
          </p>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- BLOQUE 10: EXPLORADOR INTERACTIVO EN VIVO                                  -->
    <!-- ========================================================================= -->
    <section class="explorer-container" id="bloque-explorador">
      <div class="section-header">
        <div>
          <div class="section-tag" id="txt-sec10-tag">NUEVO VISOR 10 · EXPLORADOR DINÁMICO EN VIVO</div>
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span id="txt-sec10-title">Explorador Interactivo de las 1.194 Mujeres de Mercado</span>
          </h2>
          <p class="section-desc" id="txt-sec10-desc">
            Filtra en tiempo real por comarca, régimen profesional, sector, tramo de edad o certificación ecológica para observar instantáneamente cómo cambian los indicadores clave y consultar los registros oficiales.
          </p>
        </div>
      </div>

      <!-- Filters Row -->
      <div class="filter-grid">
        <div class="filter-group">
          <label class="filter-label" for="f-comarca">Comarca (ADR)</label>
          <select id="f-comarca" class="filter-select" onchange="applyExplorerFilters()">
            <option value="ALL">Todas las Comarcas</option>
            <option value="Enkarterrialde">Enkarterrialde</option>
            <option value="Jata Ondo">Jata Ondo (Uribe)</option>
            <option value="Gorbeialde">Gorbeialde</option>
            <option value="Urremendi">Urremendi (Busturialdea)</option>
            <option value="Urkiola">Urkiola (Durangaldea)</option>
            <option value="Lea-Artibai">Lea-Artibai</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="f-regimen">Régimen Agrario</label>
          <select id="f-regimen" class="filter-select" onchange="applyExplorerFilters()">
            <option value="ALL">Ambos Regímenes (ATP y No ATP)</option>
            <option value="ATP">Solo Profesionales (ATP)</option>
            <option value="NO ATP">Solo Comerciales (NO ATP)</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="f-sector">Orientación (OTE)</label>
          <select id="f-sector" class="filter-select" onchange="applyExplorerFilters()">
            <option value="ALL">Todos los Sectores</option>
            <option value="Bovino Carne">Bovino Carne</option>
            <option value="Bovino Leche">Bovino Leche</option>
            <option value="Ovino">Ovino</option>
            <option value="Huerta Invernadero">Huerta Invernadero</option>
            <option value="Huerta Aire Libre">Huerta Aire Libre</option>
            <option value="Fruticultura">Fruticultura</option>
            <option value="Viticultura">Viticultura</option>
            <option value="Avicultura">Avicultura</option>
            <option value="Caprino">Caprino</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="f-edad">Tramo de Edad</label>
          <select id="f-edad" class="filter-select" onchange="applyExplorerFilters()">
            <option value="ALL">Todas las Edades</option>
            <option value="18-40">18 - 40 años (Jóvenes)</option>
            <option value="41-65">41 - 65 años (Maduras)</option>
            <option value=">65">> 65 años (Jubilación)</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="f-eco">Ecológico</label>
          <select id="f-eco" class="filter-select" onchange="applyExplorerFilters()">
            <option value="ALL">Todos los Modelos</option>
            <option value="SI">Solo Certificado / Proceso Eco</option>
            <option value="NO">Solo Convencional</option>
          </select>
        </div>
      </div>

      <!-- Reactive Metrics Row -->
      <div class="explorer-metrics-row">
        <div class="exp-metric-card">
          <div class="exp-metric-val" id="exp-res-total">1.194</div>
          <div class="exp-metric-lbl">Mujeres Filtradas</div>
        </div>
        <div class="exp-metric-card">
          <div class="exp-metric-val" id="exp-res-atpshare" style="color:var(--atp-primary);">15,9%</div>
          <div class="exp-metric-lbl">Tasa ATP (Profesional)</div>
        </div>
        <div class="exp-metric-card">
          <div class="exp-metric-val" id="exp-res-avgage">63,9 años</div>
          <div class="exp-metric-lbl">Edad Media</div>
        </div>
        <div class="exp-metric-card">
          <div class="exp-metric-val" id="exp-res-avgsup">11,2 ha</div>
          <div class="exp-metric-lbl">Superficie Media</div>
        </div>
        <div class="exp-metric-card">
          <div class="exp-metric-val" id="exp-res-ecos">40</div>
          <div class="exp-metric-lbl">Explotaciones Eco</div>
        </div>
      </div>

      <!-- Search Input & Table Container -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <input type="text" id="f-search" placeholder="Buscar por municipio o actividad..." 
               style="padding:8px 14px; border:1px solid var(--slate-300); border-radius:8px; width:320px; font-size:13px;"
               oninput="applyExplorerFilters()">
        <span id="exp-records-count" style="font-size:12.5px; color:var(--slate-500); font-weight:600;">
          Mostrando 1.194 registros
        </span>
      </div>

      <div class="explorer-table-wrap">
        <table class="data-table" id="exp-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Municipio</th>
              <th>Comarca</th>
              <th>Régimen</th>
              <th>Orientación (OTE)</th>
              <th>Edad</th>
              <th>Superficie</th>
              <th>Ecológico</th>
              <th>UTAs</th>
            </tr>
          </thead>
          <tbody id="exp-table-body">
            <!-- Dynamic rows inserted via JavaScript -->
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <!-- INSTITUTIONAL FOOTER -->
  <footer class="gov-footer">
    <div class="footer-content">
      <div>
        <div style="font-weight:700; color:#FFFFFF; margin-bottom:4px;">
          Diputación Foral de Bizkaia · Bizkaiko Foru Aldundia
        </div>
        <div>
          Departamento de Medio Natural y Agricultura · Nekazaritza eta Natura Ingurune Saila
        </div>
      </div>
      <div style="text-align:right;">
        <div>Estudio elaborado y diseñado por <strong>Amaterra</strong></div>
        <div style="font-size:11.5px; opacity:0.75; margin-top:2px;">
          Fuente de datos: Registro Oficial de Altas de Explotaciones de Bizkaia · Septiembre 2026
        </div>
      </div>
    </div>
  </footer>

  <!-- ========================================================================= -->
  <!-- CLIENT JAVASCRIPT & DATA STORAGE                                          -->
  <!-- ========================================================================= -->
  <script>
    // Embedded microdata of the 1,194 women with commercial holdings
    const WOMEN_DATA = """ + dataset_json_str + """;

    // Chart instances storage
    let chartInstances = {};

    // Current State
    let CURRENT_LANG = 'es';
    let CURRENT_VIEW_MODE = 'dual'; // 'dual', 'all', 'atp', 'noatp'
    let CURRENT_FUNNEL_STEP = 1;

    // Bilingual Dictionary
    const I18N = {
      es: {
        govBrand: "BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA",
        printBtn: "Imprimir / PDF",
        heroBadge: "OBSERVATORIO DE GÉNERO Y ESTRUCTURA AGRARIA · INFORME FORAL BIZKAIA · AMATERRA",
        heroTitle: "Visor Analítico: Las Mujeres en el Sector Agrario de Bizkaia",
        heroSubtitle: "Desglose metodológico en 3 fases: desde el censo global (12.120 explotaciones), el filtrado del autoconsumo (3.322 de mercado) y la diferenciación cualitativa entre el segmento profesional <strong>ATP (190 mujeres)</strong> y el colectivo comercial <strong>No ATP (1.004 mujeres)</strong>.",
        viewDual: "Comparativa Dual (Lado a Lado)",
        viewAll: "Total Mujeres Mercado (1.194)",
        viewAtp: "Solo ATP (190)",
        viewNoatp: "Solo NO ATP (1.004)",
      },
      eu: {
        govBrand: "BIZKAIKO FORU ALDUNDIA · DIPUTACIÓN FORAL DE BIZKAIA",
        printBtn: "Inprimatu / PDF",
        heroBadge: "GENERO BEHATOKIA ETA NEKAZARITZA EGITURA · FORU TXOSTENA · AMATERRA",
        heroTitle: "Bistaratzaile Analitikoa: Emakumeak Bizkaiko Nekazaritza Sektorean",
        heroSubtitle: "3 fasetako banaketa metodologikoa: errolda orokorretik (12.120 ustiapen), autokontsumoaren bereizketa (merkatuko 3.322) eta <strong>ATP profesionalen (190 emakume)</strong> eta merkataritzako <strong>No ATP kolektiboaren (1.004 emakume)</strong> arteko ezaugarritze kualitatiboa.",
        viewDual: "Konparaketa Bikoitza (Ondoz Ondo)",
        viewAll: "Merkatuko Emakume Guztiak (1.194)",
        viewAtp: "ATP Bakarrik (190)",
        viewNoatp: "NO ATP Bakarrik (1.004)",
      }
    };

    function setLang(lang) {
      CURRENT_LANG = lang;
      document.documentElement.lang = lang;
      document.getElementById('btn-lang-es').classList.toggle('active', lang === 'es');
      document.getElementById('btn-lang-eu').classList.toggle('active', lang === 'eu');
      const t = I18N[lang] || I18N.es;
      document.getElementById('txt-gov-brand').textContent = t.govBrand;
      document.getElementById('txt-print-btn').textContent = t.printBtn;
      document.getElementById('txt-hero-badge').textContent = t.heroBadge;
      document.getElementById('txt-hero-title').textContent = t.heroTitle;
      document.getElementById('txt-hero-subtitle').innerHTML = t.heroSubtitle;
      document.getElementById('txt-view-dual').textContent = t.viewDual;
      document.getElementById('txt-view-all').textContent = t.viewAll;
      document.getElementById('txt-view-atp').textContent = t.viewAtp;
      document.getElementById('txt-view-noatp').textContent = t.viewNoatp;
    }

    // Funnel Steps Switching
    function switchFunnelStep(step) {
      CURRENT_FUNNEL_STEP = step;
      for (let s = 1; s <= 3; s++) {
        document.getElementById(`btn-step-${s}`).classList.toggle('active', s === step);
        document.getElementById(`panel-step-${s}`).classList.toggle('active', s === step);
      }
    }

    // View Mode Switching
    function setViewMode(mode) {
      CURRENT_VIEW_MODE = mode;
      document.body.className = `mode-${mode}`;
      document.getElementById('btn-view-dual').classList.toggle('active', mode === 'dual');
      document.getElementById('btn-view-all').classList.toggle('active', mode === 'all');
      document.getElementById('btn-view-atp').classList.toggle('active', mode === 'atp');
      document.getElementById('btn-view-noatp').classList.toggle('active', mode === 'noatp');

      // Adjust visibility of dual cards
      const atpCards = document.querySelectorAll('.dual-card.atp');
      const noatpCards = document.querySelectorAll('.dual-card.noatp');

      if (mode === 'dual' || mode === 'all') {
        atpCards.forEach(c => c.style.display = 'block');
        noatpCards.forEach(c => c.style.display = 'block');
      } else if (mode === 'atp') {
        atpCards.forEach(c => c.style.display = 'block');
        noatpCards.forEach(c => c.style.display = 'none');
      } else if (mode === 'noatp') {
        atpCards.forEach(c => c.style.display = 'none');
        noatpCards.forEach(c => c.style.display = 'block');
      }
    }

    // Explorer Filtering Engine
    function applyExplorerFilters() {
      const comarca = document.getElementById('f-comarca').value;
      const regimen = document.getElementById('f-regimen').value;
      const sector = document.getElementById('f-sector').value;
      const edad = document.getElementById('f-edad').value;
      const eco = document.getElementById('f-eco').value;
      const search = (document.getElementById('f-search').value || '').toLowerCase().trim();

      const filtered = WOMEN_DATA.filter(item => {
        if (comarca !== 'ALL' && item.adr !== comarca) return false;
        if (regimen !== 'ALL' && item.atp !== regimen) return false;
        if (sector !== 'ALL' && item.grp !== sector) return false;
        if (edad !== 'ALL' && item.t_edad !== edad) return false;
        if (eco !== 'ALL' && item.eco !== eco) return false;
        if (search) {
          const hay = `${item.muni} ${item.adr} ${item.ote} ${item.jur}`.toLowerCase();
          if (!hay.includes(search)) return false;
        }
        return true;
      });

      // Update summary cards
      const totalFiltered = filtered.length;
      const atpCount = filtered.filter(d => d.atp === 'ATP').length;
      const atpShare = totalFiltered > 0 ? ((atpCount / totalFiltered) * 100).toFixed(1) + '%' : '0%';
      
      const ages = filtered.map(d => d.edad).filter(a => a != null);
      const avgAge = ages.length > 0 ? (ages.reduce((a,b)=>a+b, 0)/ages.length).toFixed(1) + ' años' : '-';

      const sups = filtered.map(d => d.sup).filter(s => s != null);
      const avgSup = sups.length > 0 ? (sups.reduce((a,b)=>a+b, 0)/sups.length).toFixed(1) + ' ha' : '-';

      const ecoCount = filtered.filter(d => d.eco === 'SI').length;

      document.getElementById('exp-res-total').textContent = totalFiltered.toLocaleString('es-ES');
      document.getElementById('exp-res-atpshare').textContent = atpShare;
      document.getElementById('exp-res-avgage').textContent = avgAge;
      document.getElementById('exp-res-avgsup').textContent = avgSup;
      document.getElementById('exp-res-ecos').textContent = ecoCount.toLocaleString('es-ES');
      document.getElementById('exp-records-count').textContent = `Mostrando ${totalFiltered.toLocaleString('es-ES')} de 1.194 registros`;

      // Render table (limit to first 100 for optimal DOM performance)
      const tbody = document.getElementById('exp-table-body');
      tbody.innerHTML = '';
      const displayRows = filtered.slice(0, 100);

      displayRows.forEach(d => {
        const tr = document.createElement('tr');
        const badgeClass = d.atp === 'ATP' ? 'badge-atp' : 'badge-noatp';
        const ecoBadge = d.eco === 'SI' 
          ? '<span style="color:#059669; font-weight:700;">✓ Eco</span>' 
          : '<span style="color:#94A3B8;">Convencional</span>';

        tr.innerHTML = `
          <td><span style="color:#94A3B8; font-size:11px;">#${d.id}</span></td>
          <td><strong>${d.muni}</strong></td>
          <td>${d.adr}</td>
          <td><span class="badge ${badgeClass}" style="padding:2px 8px; font-size:11px;">${d.atp}</span></td>
          <td>${d.ote}</td>
          <td>${d.edad ? d.edad + ' a.' : '-'}</td>
          <td>${d.sup ? d.sup + ' ha' : '-'}</td>
          <td>${ecoBadge}</td>
          <td><strong>${d.utas}</strong></td>
        `;
        tbody.appendChild(tr);
      });

      if (totalFiltered > 100) {
        const trInfo = document.createElement('tr');
        trInfo.innerHTML = `<td colspan="9" style="text-align:center; color:#64748B; font-style:italic; padding:12px;">Mostrando los primeros 100 resultados de ${totalFiltered}. Refina los filtros para acotar.</td>`;
        tbody.appendChild(trInfo);
      }
    }

    // Chart Initializations
    function initCharts() {
      // 1. Funnel Step 1: Total Censo (12.120)
      const ctxF1 = document.getElementById('chartFunnelStep1').getContext('2d');
      chartInstances.f1 = new Chart(ctxF1, {
        type: 'doughnut',
        data: {
          labels: ['Hombres (8.458)', 'Mujeres (3.662)'],
          datasets: [{
            data: [8458, 3662],
            backgroundColor: ['#3B82F6', '#E11D48'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { font: { weight: '600', size: 12 } } },
            tooltip: {
              callbacks: {
                label: function(ctx) {
                  const val = ctx.raw;
                  const pct = ((val / 12120) * 100).toFixed(1);
                  return ` ${ctx.label}: ${val.toLocaleString('es-ES')} (${pct}%)`;
                }
              }
            }
          }
        }
      });

      // 2. Funnel Step 2: Quitando Autoconsumo (Horizontal Stacked Bar)
      const ctxF2 = document.getElementById('chartFunnelStep2').getContext('2d');
      chartInstances.f2 = new Chart(ctxF2, {
        type: 'bar',
        data: {
          labels: ['Autoconsumo (8.798)', 'Fines de Mercado (3.322)'],
          datasets: [
            {
              label: 'Hombres',
              data: [6330, 2128],
              backgroundColor: '#3B82F6',
              borderRadius: 6
            },
            {
              label: 'Mujeres',
              data: [2468, 1194],
              backgroundColor: '#E11D48',
              borderRadius: 6
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { stacked: true, grid: { color: '#E2E8F0' } },
            y: { stacked: true, grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '600' } } },
            tooltip: {
              callbacks: {
                label: function(ctx) {
                  const val = ctx.raw;
                  const total = ctx.dataIndex === 0 ? 8798 : 3322;
                  const pct = ((val / total) * 100).toFixed(1);
                  return ` ${ctx.dataset.label}: ${val.toLocaleString('es-ES')} (${pct}%)`;
                }
              }
            }
          }
        }
      });

      // 3. Funnel Step 3: ATP vs No ATP en Mercado
      const ctxF3 = document.getElementById('chartFunnelStep3').getContext('2d');
      chartInstances.f3 = new Chart(ctxF3, {
        type: 'bar',
        data: {
          labels: ['ATP Profesional (529)', 'No ATP Comercial (2.793)'],
          datasets: [
            {
              label: 'Hombres (64,1%)',
              data: [339, 1789],
              backgroundColor: '#64748B',
              borderRadius: 6
            },
            {
              label: 'Mujeres (35,9%)',
              data: [190, 1004],
              backgroundColor: '#E11D48',
              borderRadius: 6
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { stacked: true, grid: { color: '#E2E8F0' } },
            y: { stacked: true, grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '600' } } }
          }
        }
      });

      // 4. Subsectores Chart (Top 8 comparative)
      const ctxSub = document.getElementById('chartSubsectores').getContext('2d');
      chartInstances.sub = new Chart(ctxSub, {
        type: 'bar',
        data: {
          labels: [
            'Bovinos carne', 'Bovinos leche', 'Huerta invernadero',
            'Aves ponedoras', 'Ovinos', 'Huerta aire libre',
            'Fruticultura', 'Viticultura'
          ],
          datasets: [
            {
              label: 'Mujeres ATP (190)',
              data: [43.68, 13.16, 8.95, 5.79, 4.74, 4.74, 4.74, 3.68],
              backgroundColor: '#059669',
              borderRadius: 6
            },
            {
              label: 'Mujeres NO ATP (1.004)',
              data: [44.62, 1.00, 5.98, 0.80, 12.15, 7.77, 5.78, 3.59],
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: v => v + '%' },
              grid: { color: '#F1F5F9' }
            },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '700' } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(2)}%`
              }
            }
          }
        }
      });

      // 5. Superficie Chart
      const ctxSup = document.getElementById('chartSuperficie').getContext('2d');
      chartInstances.sup = new Chart(ctxSup, {
        type: 'bar',
        data: {
          labels: ['Muy pequeña (0,5 - 5 ha)', 'Pequeña (5 - 20 ha)', 'Mediana (20 - 50 ha)', 'Grande (> 50 ha)'],
          datasets: [
            {
              label: 'Mujeres ATP (190)',
              data: [32.11, 27.37, 26.32, 14.21],
              backgroundColor: '#059669',
              borderRadius: 6
            },
            {
              label: 'Mujeres NO ATP (1.004)',
              data: [74.60, 19.82, 4.98, 0.60],
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: v => v + '%' },
              grid: { color: '#F1F5F9' }
            },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '700' } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(2)}%`
              }
            }
          }
        }
      });

      // 6. Eco Rate Chart
      const ctxEcoRate = document.getElementById('chartEcoRate').getContext('2d');
      chartInstances.ecoRate = new Chart(ctxEcoRate, {
        type: 'bar',
        data: {
          labels: ['Mujeres ATP (190)', 'Mujeres NO ATP (1.004)'],
          datasets: [{
            label: '% Producción Ecológica',
            data: [11.58, 1.79],
            backgroundColor: ['#059669', '#D97706'],
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 15,
              ticks: { callback: v => v + '%' },
              grid: { color: '#F1F5F9' }
            },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.raw.toFixed(2)}% de las mujeres son ecológicas`
              }
            }
          }
        }
      });

      // 7. Eco Gender Share Chart
      const ctxEcoGender = document.getElementById('chartEcoGenderShare').getContext('2d');
      chartInstances.ecoGender = new Chart(ctxEcoGender, {
        type: 'doughnut',
        data: {
          labels: ['Mujeres ATP Eco (22)', 'Hombres ATP Eco (32)'],
          datasets: [{
            data: [22, 32],
            backgroundColor: ['#E11D48', '#3B82F6'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { font: { weight: '600' } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.label}: ${ctx.raw} (${((ctx.raw/54)*100).toFixed(1)}%)`
              }
            }
          }
        }
      });

      // 8. Comarcas Chart
      const ctxCom = document.getElementById('chartComarcas').getContext('2d');
      chartInstances.com = new Chart(ctxCom, {
        type: 'bar',
        data: {
          labels: ['Enkarterrialde', 'Jata Ondo', 'Gorbeialde', 'Urremendi', 'Urkiola', 'Lea-Artibai'],
          datasets: [
            {
              label: 'Mujeres ATP (190)',
              data: [41.05, 16.32, 15.26, 10.53, 10.00, 6.84],
              backgroundColor: '#059669',
              borderRadius: 6
            },
            {
              label: 'Mujeres NO ATP (1.004)',
              data: [20.82, 26.00, 14.54, 14.54, 11.25, 12.85],
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: v => v + '%' },
              grid: { color: '#F1F5F9' }
            },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '700' } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(2)}%`
              }
            }
          }
        }
      });

      // 9. Juridica ATP
      const ctxJurATP = document.getElementById('chartJuridicaATP').getContext('2d');
      chartInstances.jurATP = new Chart(ctxJurATP, {
        type: 'doughnut',
        data: {
          labels: ['Persona física (80,0%)', 'Comunidad de bienes (9,5%)', 'Sociedad civil (6,3%)', 'Titularidad compartida (1,6%)', 'Otras (2,6%)'],
          datasets: [{
            data: [152, 18, 12, 3, 5],
            backgroundColor: ['#059669', '#10B981', '#6EE7B7', '#DC2626', '#CBD5E1'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } }
        }
      });

      // 10. Juridica No ATP
      const ctxJurNoATP = document.getElementById('chartJuridicaNoATP').getContext('2d');
      chartInstances.jurNoATP = new Chart(ctxJurNoATP, {
        type: 'doughnut',
        data: {
          labels: ['Persona física (95,2%)', 'Sociedad limitada (2,2%)', 'Comunidad de bienes (0,8%)', 'Sociedad civil (0,8%)', 'Otras (1,0%)'],
          datasets: [{
            data: [956, 22, 8, 8, 10],
            backgroundColor: ['#D97706', '#F59E0B', '#FCD34D', '#FEF3C7', '#E2E8F0'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } }
        }
      });

      // 11. Edad Chart
      const ctxEdad = document.getElementById('chartEdad').getContext('2d');
      chartInstances.edad = new Chart(ctxEdad, {
        type: 'bar',
        data: {
          labels: ['Jóvenes (18 - 40 años)', 'Edad Madura (41 - 65 años)', 'Jubilación (> 65 años)'],
          datasets: [
            {
              label: 'Mujeres ATP (Media 53 años)',
              data: [17.37, 68.95, 13.68],
              backgroundColor: '#059669',
              borderRadius: 6
            },
            {
              label: 'Mujeres NO ATP (Media 66 años)',
              data: [5.18, 42.33, 52.49],
              backgroundColor: '#D97706',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: v => v + '%' },
              grid: { color: '#F1F5F9' }
            },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'top', labels: { font: { weight: '700' } } },
            tooltip: {
              callbacks: {
                label: ctx => ` ${ctx.dataset.label}: ${ctx.raw.toFixed(2)}%`
              }
            }
          }
        }
      });
    }

    // Initialize application on load
    window.addEventListener('DOMContentLoaded', () => {
      initCharts();
      applyExplorerFilters();
    });
  </script>
</body>
</html>
"""

# Write to file
target_filename = "visor_mujeres_agro_bizkaia.html"
with open(target_filename, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"File {target_filename} generated successfully. File size: {os.path.getsize(target_filename)/1024:.1f} KB")
