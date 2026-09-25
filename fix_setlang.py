# fix_setlang.py

with open('reporte_diputacion_agro_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_setlang_start = "    function setLang(lang) {"
old_setlang_end = "      // Update Chart.js datasets & labels\n      updateChartsLanguage();\n    }"

start_pos = content.find(old_setlang_start)
end_pos = content.find(old_setlang_end) + len(old_setlang_end)

assert start_pos != -1 and end_pos != -1

new_setlang = """    function setLang(lang) {
      CURRENT_LANG = lang;

      const setElText = (id, text) => {
        const el = document.getElementById(id);
        if (el && text !== undefined) el.textContent = text;
      };
      const setElHtml = (id, html) => {
        const el = document.getElementById(id);
        if (el && html !== undefined) el.innerHTML = html;
      };

      document.getElementById('btn-lang-es').classList.toggle('active', lang === 'es');
      document.getElementById('btn-lang-eu').classList.toggle('active', lang === 'eu');

      const t = I18N[lang] || I18N.es;

      // Top bar & Hero
      setElText('txt-gov-brand', t.govBrand);
      setElText('txt-print-btn', t.printBtn);
      setElText('txt-hero-badge', t.heroBadge);
      setElText('txt-hero-title', t.heroTitle);
      setElHtml('txt-hero-subtitle', t.heroSubtitle);

      setElText('txt-kpi1-lbl', t.kpi1Lbl);
      setElText('txt-kpi1-desc', t.kpi1Desc);
      setElText('txt-kpi2-lbl', t.kpi2Lbl);
      setElText('txt-kpi2-desc', t.kpi2Desc);
      setElText('txt-kpi3-lbl', t.kpi3Lbl);
      setElText('txt-kpi3-val', t.kpi3Val);
      setElText('txt-kpi3-desc', t.kpi3Desc);
      setElText('txt-kpi4-lbl', t.kpi4Lbl);
      setElText('txt-kpi4-val', t.kpi4Val);
      setElText('txt-kpi4-desc', t.kpi4Desc);

      // Nav buttons
      setElText('txt-view-dual', t.viewDual);
      setElText('txt-view-atp', t.viewAtp);
      setElText('txt-view-noatp', t.viewNoatp);

      setElText('nav-chip-1', t.navChip1);
      setElText('nav-chip-2', t.navChip2);
      setElText('nav-chip-3', t.navChip3);
      setElText('nav-chip-4', t.navChip4);
      setElText('nav-chip-5', t.navChip5);

      for (let i = 1; i <= 6; i++) {
        setElText('badge-atp-pill-' + i, t.badgeAtpPill);
        setElText('badge-noatp-pill-' + i, t.badgeNoatpPill);
      }

      // Bloque 1
      setElText('txt-sec1-tag', t.sec1Tag);
      setElText('txt-sec1-title', t.sec1Title);
      setElHtml('txt-sec1-desc', t.sec1Desc);
      setElText('txt-sec1-chart-title', t.sec1ChartTitle);
      setElText('txt-sec1-chart-badge', t.sec1ChartBadge);
      setElText('txt-sec1-atp-card-title', t.sec1AtpCardTitle);
      setElText('txt-sec1-atp-base', t.sec1AtpBase);
      setElText('txt-sec1-atp-btn', t.sec1AtpBtn);
      setElText('txt-sec1-noatp-card-title', t.sec1NoatpCardTitle);
      setElText('txt-sec1-noatp-base', t.sec1NoatpBase);
      setElText('txt-sec1-noatp-btn', t.sec1NoatpBtn);
      setElText('txt-sec1-insight-title', t.sec1InsightTitle);
      setElHtml('txt-sec1-insight-text', t.sec1InsightText);

      setElText('th-sub-atp-name', t.thSubsector);
      setElText('th-sub-atp-h', t.thHombres);
      setElText('th-sub-atp-m', t.thMujeres);
      setElText('th-sub-atp-pct', t.thPctMujeresAtp);
      setElText('th-sub-noatp-name', t.thSubsector);
      setElText('th-sub-noatp-h', t.thHombres);
      setElText('th-sub-noatp-m', t.thMujeres);
      setElText('th-sub-noatp-pct', t.thPctMujeresNoatp);

      // Bloque 2
      setElText('txt-sec2-tag', t.sec2Tag);
      setElText('txt-sec2-title', t.sec2Title);
      setElHtml('txt-sec2-desc', t.sec2Desc);
      setElText('txt-sec2-chart-title', t.sec2ChartTitle);
      setElText('txt-sec2-chart-badge', t.sec2ChartBadge);
      setElText('txt-sec2-atp-card-title', t.sec2AtpCardTitle);
      setElText('txt-sec2-atp-base', t.sec2AtpBase);
      setElText('txt-sec2-noatp-card-title', t.sec2NoatpCardTitle);
      setElText('txt-sec2-noatp-base', t.sec2NoatpBase);
      setElText('txt-sec2-insight-title', t.sec2InsightTitle);
      setElHtml('txt-sec2-insight-text', t.sec2InsightText);

      // Bloque 3
      setElText('txt-sec3-tag', t.sec3Tag);
      setElText('txt-sec3-title', t.sec3Title);
      setElHtml('txt-sec3-desc', t.sec3Desc);
      setElText('txt-sec3-atp-card-title', t.sec3AtpCardTitle);
      setElText('txt-sec3-atp-base', t.sec3AtpBase);
      setElText('txt-sec3-atp-unit', t.sec3AtpUnit);
      setElHtml('txt-sec3-atp-text', t.sec3AtpText);
      setElHtml('txt-sec3-atp-note', t.sec3AtpNote);

      // Bloque 4
      setElText('txt-sec4-tag', t.sec4Tag);
      setElText('txt-sec4-title', t.sec4Title);
      setElHtml('txt-sec4-desc', t.sec4Desc);
      setElText('txt-sec4-chart-title', t.sec4ChartTitle);
      setElText('txt-sec4-chart-badge', t.sec4ChartBadge);
      setElText('txt-sec4-insight-title', t.sec4InsightTitle);
      setElHtml('txt-sec4-insight-text', t.sec4InsightText);

      // Bloque 5
      setElText('txt-sec6-tag', t.sec6Tag);
      setElText('txt-sec6-title', t.sec6Title);
      setElHtml('txt-sec6-desc', t.sec6Desc);
      setElText('txt-sec6-atp-card-title', t.sec6AtpCardTitle);
      setElText('txt-sec6-atp-base', t.sec6AtpBase);
      setElText('txt-sec6-atp-unit', t.sec6AtpUnit);
      setElText('txt-sec6-noatp-card-title', t.sec6NoatpCardTitle);
      setElText('txt-sec6-noatp-base', t.sec6NoatpBase);
      setElText('txt-sec6-noatp-unit', t.sec6NoatpUnit);
      setElText('txt-sec6-insight-title', t.sec6InsightTitle);
      setElHtml('txt-sec6-insight-text', t.sec6InsightText);

      // Footer
      setElText('txt-footer-title', t.footerTitle);
      setElText('txt-footer-source', t.footerSource);
      setElText('txt-footer-amaterra', t.footerAmaterra);
      setElText('txt-footer-link-1', t.navChip1.replace(/^\\d+\\.\\s*/, ''));
      setElText('txt-footer-link-2', t.navChip2.replace(/^\\d+\\.\\s*/, ''));
      setElText('txt-footer-link-3', t.navChip3.replace(/^\\d+\\.\\s*/, ''));
      setElText('txt-footer-link-4', t.navChip4.replace(/^\\d+\\.\\s*/, ''));
      setElText('txt-footer-link-5', t.navChip5.replace(/^\\d+\\.\\s*/, ''));

      // Re-render dynamic lists with translated item labels
      renderSubsectores();
      renderSuperficie();
      renderEcologico();
      renderComarcas();
      renderEdad();

      // Update Chart.js datasets & labels
      updateChartsLanguage();
    }"""

updated_content = content[:start_pos] + new_setlang + content[end_pos:]

with open('reporte_diputacion_agro_2.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("setLang successfully hardened!")
