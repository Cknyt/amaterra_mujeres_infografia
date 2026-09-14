"""Módulo de visualización de datos agrarios (src/visualizer.py).

Diseñado con un enfoque editorial 'De Macro a Micro':
- Nivel 1: Macro-embudo mediante Diagrama de Sankey (Mercado -> ATP/No ATP -> Hombres/Mujeres).
- Nivel 2: Zoom comparativo demográfico y económico (Pirámide divergente de edad, Dumbbell de brechas ha/UTAs, Desglose ecológico).
- Nivel 3: Detalle sectorial (Subsectores OTE UE) y formas jurídicas.
- Nivel 4: Distribución y ranking territorial comarcal con benchmark medio regional.

Todas las funciones generan objetos go.Figure listos para Streamlit o exportación en alta resolución (PNG 300 DPI / SVG / PPTX).
"""

from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Asegurar que el directorio raíz esté en sys.path al ejecutar como script independiente
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Paleta cromática editorial por defecto
DEFAULT_PALETTE = {
    "hombre": "#2B6CB0",        # Azul grafito / Slate Blue
    "mujer": "#805AD5",         # Morado / Violeta editorial
    "hombres": "#2B6CB0",
    "mujeres": "#805AD5",
    "atp": "#2D6A4F",           # Verde bosque profesional
    "no_atp": "#718096",        # Gris pizarra neutral
    "accent_m": "#D53F8C",      # Magenta acento
    "teal": "#2C7A7B",          # Teal / Esmeralda
    "neutral_dark": "#2D3748",  # Texto principal
    "neutral_muted": "#718096", # Texto secundario / anotaciones
    "grid": "#F0F2F5",          # Rejilla suave
    "bg": "#FFFFFF",            # Fondo limpio
}


def _apply_editorial_theme(
    fig: go.Figure,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    show_legend: bool = True,
    height: int = 500,
) -> go.Figure:
    """Aplica la configuración visual y tipográfica homogénea al gráfico."""
    formatted_title = None
    if title:
        if subtitle:
            muted_color = DEFAULT_PALETTE["neutral_muted"]
            formatted_title = (
                f"<b>{title}</b><br>"
                f"<span style='font-size:12px;color:{muted_color};font-weight:normal;'>"
                f"{subtitle}</span>"
            )
        else:
            formatted_title = f"<b>{title}</b>"

    fig.update_layout(
        title=dict(
            text=formatted_title,
            x=0.03,
            y=0.96,
            xanchor="left",
            yanchor="top",
            font=dict(
                family="Segoe UI, -apple-system, Roboto, sans-serif",
                size=16,
                color=DEFAULT_PALETTE["neutral_dark"],
            ),
        ),
        paper_bgcolor=DEFAULT_PALETTE["bg"],
        plot_bgcolor=DEFAULT_PALETTE["bg"],
        font=dict(
            family="Segoe UI, -apple-system, Roboto, sans-serif",
            size=12,
            color=DEFAULT_PALETTE["neutral_dark"],
        ),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.98,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.05)",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=40, r=40, t=75 if subtitle else 60, b=40),
    )
    return fig


# ==============================================================================
# NIVEL 1: EL MACRO-EMBUDO (Sankey Diagram)
# ==============================================================================

def build_sankey_overview(
    macro_kpis: Dict[str, Any],
    color_h: Optional[str] = None,
    color_m: Optional[str] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 500,
    show_legend: bool = False,
    colors: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Construye el diagrama de flujo Sankey para el Macro-Embudo de explotaciones de mercado."""
    ch = color_h or (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = color_m or (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    total = macro_kpis.get("total_comerciales", 3323)
    atp_total = macro_kpis.get("total_atp", 529)
    no_atp_total = macro_kpis.get("total_no_atp", 2794)

    atp_stats = macro_kpis.get("atp", {})
    no_atp_stats = macro_kpis.get("no_atp", {})

    atp_h = atp_stats.get("hombres", 339)
    atp_m = atp_stats.get("mujeres", 190)
    no_atp_h = no_atp_stats.get("hombres", 1790)
    no_atp_m = no_atp_stats.get("mujeres", 1004)

    node_labels = [
        f"<b>Mercado Comercial</b><br>{total:,} expl. (100%)",
        f"<b>ATP</b><br>{atp_total:,} ({round(atp_total/total*100, 1)}%)",
        f"<b>No ATP</b><br>{no_atp_total:,} ({round(no_atp_total/total*100, 1)}%)",
        f"<b>ATP · Hombres</b><br>{atp_h:,} ({round(atp_h/atp_total*100, 1)}%)",
        f"<b>ATP · Mujeres</b><br>{atp_m:,} ({round(atp_m/atp_total*100, 1)}%)",
        f"<b>No ATP · Hombres</b><br>{no_atp_h:,} ({round(no_atp_h/no_atp_total*100, 1)}%)",
        f"<b>No ATP · Mujeres</b><br>{no_atp_m:,} ({round(no_atp_m/no_atp_total*100, 1)}%)",
    ]

    node_colors = [
        "#1B4332",                  # Mercado
        DEFAULT_PALETTE["atp"],     # ATP
        DEFAULT_PALETTE["no_atp"],  # No ATP
        ch,                         # ATP H
        cm,                         # ATP M
        "#4A5568",                  # No ATP H
        "#D53F8C",                  # No ATP M
    ]

    sources = [0, 0, 1, 1, 2, 2]
    targets = [1, 2, 3, 4, 5, 6]
    values = [atp_total, no_atp_total, atp_h, atp_m, no_atp_h, no_atp_m]

    link_colors = [
        "rgba(45, 106, 79, 0.35)",   # Mercado -> ATP
        "rgba(113, 128, 150, 0.30)", # Mercado -> No ATP
        "rgba(43, 108, 176, 0.45)",  # ATP -> H
        "rgba(128, 90, 213, 0.45)",  # ATP -> M
        "rgba(74, 85, 104, 0.35)",   # No ATP -> H
        "rgba(213, 63, 140, 0.35)",  # No ATP -> M
    ]

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=22,
                    thickness=24,
                    line=dict(color="rgba(0,0,0,0.15)", width=1),
                    label=node_labels,
                    color=node_colors,
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                ),
            )
        ]
    )

    t = title or "Macro-Embudo de Explotaciones Agrarias Comerciales"
    st = subtitle or "Distribución del tejido productivo según Profesionalidad (ATP vs No ATP) y Titularidad de Género"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


# ==============================================================================
# NIVEL 2: ZOOM COMPARATIVO (Demografía y Dimensión)
# ==============================================================================

def build_age_pyramid_divergent(
    df_age: pd.DataFrame,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    colors: Optional[Dict[str, str]] = None,
    height: int = 500,
    show_legend: bool = True,
) -> go.Figure:
    """Construye una pirámide demográfica divergente para tramos de edad enfrentando Hombres vs Mujeres."""
    ch = (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    categories = df_age["Tramo"].tolist()
    hombres_vals = df_age["Hombres"].tolist()
    mujeres_vals = df_age["Mujeres"].tolist()
    pct_fem = df_age["% Feminización"].tolist()

    fig = go.Figure()

    # Barra Hombres (valores negativos para orientar a la izquierda)
    fig.add_trace(
        go.Bar(
            y=categories,
            x=[-h for h in hombres_vals],
            name="Hombres",
            orientation="h",
            marker=dict(color=ch, line=dict(color="rgba(0,0,0,0.1)", width=1)),
            text=[f"{h:,}" for h in hombres_vals],
            textposition="inside",
            insidetextanchor="middle",
            hoverinfo="y+text",
            hovertext=[f"<b>Hombres:</b> {h:,} ({round(h/max(1,h+m)*100, 1)}%)" for h, m in zip(hombres_vals, mujeres_vals)],
        )
    )

    # Barra Mujeres (valores positivos hacia la derecha)
    fig.add_trace(
        go.Bar(
            y=categories,
            x=mujeres_vals,
            name="Mujeres",
            orientation="h",
            marker=dict(color=cm, line=dict(color="rgba(0,0,0,0.1)", width=1)),
            text=[f"{m:,} ({p:.1f}%)" for m, p in zip(mujeres_vals, pct_fem)],
            textposition="inside",
            insidetextanchor="middle",
            hoverinfo="y+text",
            hovertext=[f"<b>Mujeres:</b> {m:,} ({p:.1f}%)" for m, p in zip(mujeres_vals, pct_fem)],
        )
    )

    # Añadir marcadores exteriores con la tasa de feminización
    for idx, (cat, m_val, fem) in enumerate(zip(categories, mujeres_vals, pct_fem)):
        fig.add_annotation(
            x=m_val + (max(mujeres_vals) * 0.05),
            y=cat,
            text=f"<b>{fem:.1f}% M</b>",
            showarrow=False,
            font=dict(color=cm, size=11),
            xanchor="left",
        )

    # Eje X simétrico
    max_x = max(max(hombres_vals), max(mujeres_vals)) * 1.25
    tick_vals = np.linspace(-max_x, max_x, 7)
    tick_text = [f"{abs(int(v)):,}" for v in tick_vals]

    fig.update_layout(
        barmode="relative",
        bargap=0.18,
        xaxis=dict(
            title="Número de Explotaciones",
            tickvals=tick_vals,
            ticktext=tick_text,
            gridcolor=DEFAULT_PALETTE["grid"],
            zeroline=True,
            zerolinecolor="#4A5568",
            zerolinewidth=1.5,
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=categories[::-1],
        ),
    )

    t = title or "Pirámide Demográfica y Brecha Generacional por Género"
    st = subtitle or "Estructura por edad de los titulares: resalta la concentración de mujeres en edades avanzadas"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


def build_dumbbell_economic_gap(
    kpis: Dict[str, Any],
    metric: str = "both",
    colors: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 420,
    show_legend: bool = True,
) -> go.Figure:
    """Construye un gráfico de mancuerna (dumbbell plot) ilustrando la brecha de género en superficie y UTAs."""
    ch = (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    segments = ["No ATP", "ATP"]

    if metric == "both":
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Superficie Media (ha)", "Unidades de Trabajo Agrario (UTAs Medias)"),
            horizontal_spacing=0.14,
        )

        for i, seg in enumerate(segments):
            seg_key = "atp" if seg == "ATP" else "no_atp"
            data_seg = kpis.get(seg_key, {})

            sup_h = data_seg.get("superficie_media_hombres", 0.0)
            sup_m = data_seg.get("superficie_media_mujeres", 0.0)
            gap_sup = data_seg.get("brecha_superficie_pct", 0.0)

            utas_h = data_seg.get("utas_media_hombres", 0.0)
            utas_m = data_seg.get("utas_media_mujeres", 0.0)
            gap_utas = data_seg.get("brecha_utas_pct", 0.0)

            # --- Columna 1: Superficie ---
            fig.add_trace(
                go.Scatter(
                    x=[sup_m, sup_h],
                    y=[seg, seg],
                    mode="lines",
                    line=dict(color="#CBD5E0", width=4),
                    showlegend=False,
                    hoverinfo="none",
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=[sup_h],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=ch, size=14, line=dict(color="white", width=1.5)),
                    text=[f"{sup_h:.1f} ha"],
                    textposition="top center",
                    name="Hombres",
                    showlegend=(i == 0),
                    hoverinfo="text",
                    hovertext=f"Hombres ({seg}): {sup_h:.2f} ha",
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=[sup_m],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=cm, size=14, line=dict(color="white", width=1.5)),
                    text=[f"{sup_m:.1f} ha"],
                    textposition="top center",
                    name="Mujeres",
                    showlegend=(i == 0),
                    hoverinfo="text",
                    hovertext=f"Mujeres ({seg}): {sup_m:.2f} ha",
                ),
                row=1,
                col=1,
            )
            fig.add_annotation(
                x=(sup_h + sup_m) / 2,
                y=seg,
                text=f"<b>-{gap_sup:.1f}%</b>",
                showarrow=False,
                yshift=-18,
                font=dict(color="#C53030", size=11),
                row=1,
                col=1,
            )

            # --- Columna 2: UTAs ---
            fig.add_trace(
                go.Scatter(
                    x=[utas_m, utas_h],
                    y=[seg, seg],
                    mode="lines",
                    line=dict(color="#CBD5E0", width=4),
                    showlegend=False,
                    hoverinfo="none",
                ),
                row=1,
                col=2,
            )
            fig.add_trace(
                go.Scatter(
                    x=[utas_h],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=ch, size=14, line=dict(color="white", width=1.5)),
                    text=[f"{utas_h:.2f}"],
                    textposition="top center",
                    showlegend=False,
                    hoverinfo="text",
                    hovertext=f"Hombres ({seg}): {utas_h:.2f} UTAs",
                ),
                row=1,
                col=2,
            )
            fig.add_trace(
                go.Scatter(
                    x=[utas_m],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=cm, size=14, line=dict(color="white", width=1.5)),
                    text=[f"{utas_m:.2f}"],
                    textposition="top center",
                    showlegend=False,
                    hoverinfo="text",
                    hovertext=f"Mujeres ({seg}): {utas_m:.2f} UTAs",
                ),
                row=1,
                col=2,
            )
            fig.add_annotation(
                x=(utas_h + utas_m) / 2,
                y=seg,
                text=f"<b>-{gap_utas:.1f}%</b>",
                showarrow=False,
                yshift=-18,
                font=dict(color="#C53030", size=11),
                row=1,
                col=2,
            )

        fig.update_xaxes(gridcolor=DEFAULT_PALETTE["grid"], zeroline=False)
        fig.update_yaxes(autorange="reversed")

    else:
        # Modo simple para una única métrica
        is_sup = "sup" in metric.lower()
        fig = go.Figure()

        for i, seg in enumerate(segments):
            seg_key = "atp" if seg == "ATP" else "no_atp"
            data_seg = kpis.get(seg_key, {})
            val_h = data_seg.get("superficie_media_hombres" if is_sup else "utas_media_hombres", 0.0)
            val_m = data_seg.get("superficie_media_mujeres" if is_sup else "utas_media_mujeres", 0.0)
            gap = data_seg.get("brecha_superficie_pct" if is_sup else "brecha_utas_pct", 0.0)
            unit = "ha" if is_sup else "UTAs"

            fig.add_trace(
                go.Scatter(
                    x=[val_m, val_h],
                    y=[seg, seg],
                    mode="lines",
                    line=dict(color="#CBD5E0", width=4),
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[val_h],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=ch, size=14),
                    text=[f"{val_h:.1f} {unit}"],
                    textposition="top center",
                    name="Hombres",
                    showlegend=(i == 0),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[val_m],
                    y=[seg],
                    mode="markers+text",
                    marker=dict(color=cm, size=14),
                    text=[f"{val_m:.1f} {unit}"],
                    textposition="top center",
                    name="Mujeres",
                    showlegend=(i == 0),
                )
            )
            fig.add_annotation(
                x=(val_h + val_m) / 2,
                y=seg,
                text=f"<b>-{gap:.1f}%</b>",
                showarrow=False,
                yshift=-18,
                font=dict(color="#C53030", size=11),
            )

        fig.update_xaxes(gridcolor=DEFAULT_PALETTE["grid"])
        fig.update_yaxes(autorange="reversed")

    t = title or "Brecha Económica y Productiva de Género (Dumbbell Plot)"
    st = subtitle or "Comparación de dimensión media en Superficie Agraria Útil y Mano de Obra (UTAs)"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


def build_sustainability_breakdown(
    df_eco: pd.DataFrame,
    colors: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 420,
    show_legend: bool = True,
) -> go.Figure:
    """Genera un gráfico de barras mostrando la distribución de explotaciones ecológicas por género."""
    ch = (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    categories = df_eco["Tipo Ecológico"].tolist()
    hombres = df_eco["Hombres"].tolist()
    mujeres = df_eco["Mujeres"].tolist()
    totales = df_eco["Total"].tolist()
    pct_fem = df_eco["% Feminización"].tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=categories,
            x=hombres,
            name="Hombres",
            orientation="h",
            marker=dict(color=ch),
            text=[f"{h:,}" for h in hombres],
            textposition="auto",
        )
    )

    fig.add_trace(
        go.Bar(
            y=categories,
            x=mujeres,
            name="Mujeres",
            orientation="h",
            marker=dict(color=cm),
            text=[f"{m:,} ({p:.1f}%)" for m, p in zip(mujeres, pct_fem)],
            textposition="auto",
        )
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(title="Número de Explotaciones", gridcolor=DEFAULT_PALETTE["grid"]),
        yaxis=dict(title="", categoryorder="total ascending"),
    )

    t = title or "Transición Ecológica y Sostenibilidad según Género"
    st = subtitle or "Presencia femenina en explotaciones ecológicas certificadas y en proceso de conversión"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


# ==============================================================================
# NIVEL 3: DETALLE SECTORIAL Y JURÍDICO (Micro)
# ==============================================================================

def build_subsectors_horizontal_bar(
    df_sub: pd.DataFrame,
    top_n: int = 15,
    colors: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 580,
    show_legend: bool = True,
) -> go.Figure:
    """Genera un gráfico de barras horizontales apiladas para los subsectores productivos principales."""
    ch = (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    top_df = df_sub.head(top_n).sort_values(by="Total", ascending=True)

    # Formatear nombres de subsector para una lectura óptima
    def _clean_subsector(name: str) -> str:
        s = str(name).replace("EXPLOTACIONES DE ", "").replace("EXPLOTACIONES ESPECIALIZADAS EN ", "").replace("ESPECIALIZADAS: ", "")
        s = s.capitalize()
        return s[:45] + "..." if len(s) > 48 else s

    labels = [_clean_subsector(s) for s in top_df["Subsector"]]
    hombres = top_df["Hombres"].tolist()
    mujeres = top_df["Mujeres"].tolist()
    pct_fem = top_df["% Feminización"].tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=labels,
            x=hombres,
            name="Hombres",
            orientation="h",
            marker=dict(color=ch),
            text=[f"{h}" if h > 5 else "" for h in hombres],
            textposition="inside",
        )
    )

    fig.add_trace(
        go.Bar(
            y=labels,
            x=mujeres,
            name="Mujeres",
            orientation="h",
            marker=dict(color=cm),
            text=[f"{m} ({p:.0f}%)" if m > 3 else "" for m, p in zip(mujeres, pct_fem)],
            textposition="inside",
        )
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(title="Número de Explotaciones", gridcolor=DEFAULT_PALETTE["grid"]),
        yaxis=dict(title="", automargin=True),
    )

    t = title or f"Principales Subsectores Técnico-Económicos (Top {top_n})"
    st = subtitle or "Especialización productiva y grado de feminización por tipo de explotación (OTE UE)"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


def build_legal_status_bar(
    df_legal: pd.DataFrame,
    colors: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 460,
    show_legend: bool = True,
) -> go.Figure:
    """Genera gráfico de distribución por forma jurídica destacando la presencia femenina."""
    ch = (colors.get("hombre") if colors else None) or DEFAULT_PALETTE["hombre"]
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    df_sorted = df_legal.sort_values(by="Total", ascending=True)

    labels = [str(k).title() for k in df_sorted["Condición Jurídica"]]
    hombres = df_sorted["Hombres"].tolist()
    mujeres = df_sorted["Mujeres"].tolist()
    pct_fem = df_sorted["% Feminización"].tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=labels,
            x=hombres,
            name="Hombres",
            orientation="h",
            marker=dict(color=ch),
            text=[f"{h:,}" for h in hombres],
            textposition="inside",
        )
    )

    fig.add_trace(
        go.Bar(
            y=labels,
            x=mujeres,
            name="Mujeres",
            orientation="h",
            marker=dict(color=cm),
            text=[f"{m:,} ({p:.1f}%)" for m, p in zip(mujeres, pct_fem)],
            textposition="inside",
        )
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(title="Número de Explotaciones", gridcolor=DEFAULT_PALETTE["grid"]),
        yaxis=dict(title="", automargin=True),
    )

    t = title or "Estructura Jurídica de la Explotación y Titularidad Compartida"
    st = subtitle or "Distribución según personalidad jurídica: personas físicas, sociedades y titularidad compartida"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


# ==============================================================================
# NIVEL 4: DISTRIBUCIÓN GEOGRÁFICA
# ==============================================================================

def build_territorial_ranking(
    df_territory: pd.DataFrame,
    colors: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    height: int = 460,
    show_legend: bool = True,
) -> go.Figure:
    """Construye un ranking territorial horizontal ordenado por la Razón de Feminización (M por 100 H)."""
    cm = (colors.get("mujer") if colors else None) or DEFAULT_PALETTE["mujer"]

    # Ordenar de menor a mayor para que el más alto aparezca en la parte superior
    df_sorted = df_territory.sort_values(by="Razón (M por 100 H)", ascending=True)

    col_terr = "OCA" if "OCA" in df_sorted.columns else ("Comarca" if "Comarca" in df_sorted.columns else df_sorted.columns[0])
    comarcas = df_sorted[col_terr].tolist()
    razon_vals = df_sorted["Razón (M por 100 H)"].tolist()
    mujeres = df_sorted["Mujeres"].tolist()
    hombres = df_sorted["Hombres"].tolist()
    pct_fem = df_sorted["% Feminización"].tolist()

    # Cálculo del benchmark medio regional
    total_m = sum(mujeres)
    total_h = sum(hombres)
    media_regional = round((total_m / total_h * 100), 1) if total_h > 0 else 0.0

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=comarcas,
            x=razon_vals,
            orientation="h",
            marker=dict(
                color=[cm if r >= media_regional else "#A0AEC0" for r in razon_vals],
                line=dict(color="rgba(0,0,0,0.1)", width=1),
            ),
            text=[f"<b>{r:.1f}</b> ({m} M / {h} H)" for r, m, h in zip(razon_vals, mujeres, hombres)],
            textposition="auto",
            hoverinfo="y+text",
            hovertext=[f"<b>{c}:</b> {r:.1f} mujeres por 100 hombres ({p:.1f}% feminización)" for c, r, p in zip(comarcas, razon_vals, pct_fem)],
            name="Razón M/100H",
            showlegend=False,
        )
    )

    # Línea vertical del benchmark regional
    fig.add_vline(
        x=media_regional,
        line_dash="dash",
        line_color="#E53E3E",
        line_width=2,
        annotation_text=f"Media regional: {media_regional:.1f} M por 100 H",
        annotation_position="top right",
        annotation_font=dict(color="#C53030", size=11, family="Segoe UI, sans-serif"),
    )

    fig.update_layout(
        xaxis=dict(
            title="Razón de Feminización (Mujeres por cada 100 Hombres)",
            gridcolor=DEFAULT_PALETTE["grid"],
        ),
        yaxis=dict(title=""),
    )

    t = title or f"Ranking Territorial de Feminización Agraria por {col_terr}"
    st = subtitle or f"Razón de mujeres por cada 100 hombres comparada contra el promedio regional ({media_regional:.1f})"
    return _apply_editorial_theme(fig, t, st, show_legend, height)


# ==============================================================================
# ALIAS Y COMPATIBILIDAD CON FUNCIONES PREVIAS
# ==============================================================================

def create_sankey_flow(df: pd.DataFrame, **kwargs) -> go.Figure:
    """Wrapper de compatibilidad previa para diagrama de flujo Sankey."""
    hombres = int((df["GENERO"] == "Hombre").sum())
    mujeres = int((df["GENERO"] == "Mujer").sum())
    atp_mask = df["CALIFICACION ATP"] == "ATP" if "CALIFICACION ATP" in df.columns else pd.Series(False, index=df.index)
    kpis_dummy = {
        "total_comerciales": len(df),
        "total_atp": int(atp_mask.sum()),
        "total_no_atp": int((~atp_mask).sum()),
        "atp": {
            "hombres": int((atp_mask & (df["GENERO"] == "Hombre")).sum()),
            "mujeres": int((atp_mask & (df["GENERO"] == "Mujer")).sum()),
        },
        "no_atp": {
            "hombres": int((~atp_mask & (df["GENERO"] == "Hombre")).sum()),
            "mujeres": int((~atp_mask & (df["GENERO"] == "Mujer")).sum()),
        },
    }
    return build_sankey_overview(kpis_dummy, title=kwargs.get("title"))


def create_demographic_pyramid(df: pd.DataFrame, **kwargs) -> go.Figure:
    """Wrapper de compatibilidad previa para pirámide demográfica."""
    from src.data_processor import AgrarianDataProcessor
    processor = AgrarianDataProcessor(df)
    df_age = processor.get_age_distribution(mode="4_tramos")
    return build_age_pyramid_divergent(df_age, title=kwargs.get("title"))


def create_comarca_breakdown_chart(df: pd.DataFrame, **kwargs) -> go.Figure:
    """Wrapper de compatibilidad previa para desglose comarcal."""
    from src.data_processor import AgrarianDataProcessor
    processor = AgrarianDataProcessor(df)
    df_terr = processor.get_territorial_summary()
    return build_territorial_ranking(df_terr, title=kwargs.get("title"))


def create_surface_distribution_chart(df: pd.DataFrame, **kwargs) -> go.Figure:
    """Wrapper de compatibilidad previa para distribución de superficies."""
    from src.data_processor import AgrarianDataProcessor
    processor = AgrarianDataProcessor(df)
    df_surf = processor.get_surface_strata(strata_type="agronomico")
    labels = df_surf["Estrato"].tolist()
    hombres = df_surf["Hombres"].tolist()
    mujeres = df_surf["Mujeres"].tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(y=labels, x=hombres, name="Hombres", orientation="h", marker_color=DEFAULT_PALETTE["hombre"]))
    fig.add_trace(go.Bar(y=labels, x=mujeres, name="Mujeres", orientation="h", marker_color=DEFAULT_PALETTE["mujer"]))
    fig.update_layout(barmode="stack", xaxis=dict(title="Explotaciones", gridcolor=DEFAULT_PALETTE["grid"]))
    return _apply_editorial_theme(fig, kwargs.get("title", "Distribución de Explotaciones por Superficie"), height=450)


# ==============================================================================
# TEST UNITARIO LOCAL DIRECTO (__main__)
# ==============================================================================

if __name__ == "__main__":
    from src.data_processor import AgrarianDataProcessor

    print("Iniciando validación de constructores de gráficos Plotly (src/visualizer.py)...")

    processor = AgrarianDataProcessor.from_file()
    kpis = processor.get_macro_kpis()
    df_age = processor.get_age_distribution("ALL", "4_tramos")
    df_sub = processor.get_subsectors_summary("ATP")
    df_legal = processor.get_legal_status_summary("ATP")
    df_terr = processor.get_territorial_summary("ATP")
    df_eco = processor.get_sustainability_summary("ALL")

    # 1. Nivel 1: Sankey
    f1 = build_sankey_overview(kpis)
    assert "data" in f1.to_dict(), "Fallo en estructura de Sankey"

    # 2. Nivel 2: Pirámide y Mancuerna
    f2 = build_age_pyramid_divergent(df_age)
    assert len(f2.data) >= 2, "Fallo en trazas de Pirámide divergente"

    f3 = build_dumbbell_economic_gap(kpis, metric="both")
    assert "data" in f3.to_dict(), "Fallo en Dumbbell plot"

    f4 = build_sustainability_breakdown(df_eco)
    assert len(f4.data) == 2, "Fallo en Sostenibilidad"

    # 3. Nivel 3: Subsectores y Formas Jurídicas
    f5 = build_subsectors_horizontal_bar(df_sub, top_n=10)
    assert len(f5.data) == 2, "Fallo en Subsectores"

    f6 = build_legal_status_bar(df_legal)
    assert len(f6.data) == 2, "Fallo en Formas Jurídicas"

    # 4. Nivel 4: Territorial
    f7 = build_territorial_ranking(df_terr)
    assert len(f7.data) == 1, "Fallo en Ranking territorial"

    # Validar serialización JSON de cada figura
    for i, fig in enumerate([f1, f2, f3, f4, f5, f6, f7], start=1):
        json_repr = fig.to_json()
        assert len(json_repr) > 100, f"Error en serialización JSON de figura {i}"

    print("✓ Módulo de visualizaciones Plotly verificado con éxito.")
