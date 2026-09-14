"""Bizkaia Agraria | Brecha de Género y Dimensión Productiva.

Punto de entrada interactivo principal en Streamlit.
Conecta la fuente única de verdad analítica (AgrarianDataProcessor),
el motor de gráficos editoriales (visualizer) y el orquestador de exportaciones (exporter).
"""

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import DEFAULT_EXCEL_PATH
from src.data_processor import AgrarianDataProcessor, load_and_clean_data
from src.exporter import (
    PowerPointReportBuilder,
    export_chart,
    export_tables_to_excel,
)
from src.visualizer import (
    build_age_pyramid_divergent,
    build_dumbbell_economic_gap,
    build_legal_status_bar,
    build_sankey_overview,
    build_subsectors_horizontal_bar,
    build_sustainability_breakdown,
    build_territorial_ranking,
)

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS GLOBALES
# ==============================================================================
st.set_page_config(
    page_title="Bizkaia Agraria | Brecha de Género",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyección de CSS moderno, limpio y profesional
st.markdown(
    """
    <style>
    /* Tipografía y espaciado general */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
    }
    
    /* Contenedores de tarjetas métricas (KPIs) */
    .metric-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #1F4E38;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-container-purple {
        border-left-color: #805AD5;
    }
    .metric-container-red {
        border-left-color: #C53030;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 700;
        color: #718096;
        margin-bottom: 0.3rem;
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        color: #1A202C;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.82rem;
        font-weight: 600;
        color: #4A5568;
        margin-top: 0.35rem;
    }

    /* Botón primario corporativo verde bosque */
    button[kind="primary"] {
        background-color: #1F4E38 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.2rem !important;
        transition: background-color 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #163A29 !important;
        box-shadow: 0 4px 10px rgba(31, 78, 56, 0.3) !important;
    }

    /* Pestañas modernas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #4A5568;
    }
    .stTabs [aria-selected="true"] {
        color: #1F4E38 !important;
        border-bottom: 3px solid #1F4E38 !important;
    }

    /* Tablas ejecutivas estilizadas */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.92rem;
        margin: 1rem 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .styled-table thead tr {
        background-color: #1F4E38;
        color: #FFFFFF;
        text-align: left;
        font-weight: 700;
    }
    .styled-table th, .styled-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #E2E8F0;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #F8FAFC;
    }
    .styled-table tbody tr:hover {
        background-color: #EDF2F7;
    }
    .gap-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
        color: #9B2C2C;
        background-color: #FED7D7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Paletas de color disponibles para selección interactiva
PALETTES: Dict[str, Dict[str, str]] = {
    "Corporativa": {
        "hombre": "#2B6CB0",       # Azul corporativo
        "mujer": "#805AD5",        # Morado institucional
        "name": "Corporativa (Azul / Morado)",
    },
    "Naturaleza": {
        "hombre": "#4A5568",       # Gris pizarra
        "mujer": "#2C7A7B",        # Esmeralda / Teal
        "name": "Naturaleza (Pizarra / Esmeralda)",
    },
    "Alto Contraste": {
        "hombre": "#1A365D",       # Navy oscuro
        "mujer": "#D53F8C",        # Magenta vibrante
        "name": "Alto Contraste (Navy / Magenta)",
    },
}


# ==============================================================================
# CACHÉ DE DATOS
# ==============================================================================

@st.cache_data(show_spinner=False)
def get_cached_dataset(file_bytes: Optional[bytes] = None) -> pd.DataFrame:
    """Carga y procesa el dataset con almacenamiento en memoria caché de Streamlit."""
    if file_bytes is not None:
        return load_and_clean_data(BytesIO(file_bytes))
    return load_and_clean_data(DEFAULT_EXCEL_PATH)


def main():
    # ==========================================================================
    # 2. SIDEBAR: PANEL DE CONTROL Y EDICIÓN (STUDIO PLAYGROUND)
    # ==========================================================================
    st.sidebar.title("🎛️ Studio Playground")
    st.sidebar.caption("Configuración analítica y exportación en tiempo real.")

    # --- CARGA DE DATOS ---
    st.sidebar.subheader("📁 Carga de Datos")
    data_source_mode = st.sidebar.radio(
        "Modo de Carga",
        ["Ruta por defecto (./AMATERRA_Mujeres_DatosExplotacionesAlta_Datos01.xlsx)", "Subir archivo Excel"],
        index=0,
    )

    uploaded_bytes = None
    if "Subir" in data_source_mode:
        uploaded_file = st.sidebar.file_uploader(
            "Cargar archivo .xlsx",
            type=["xlsx", "xls"],
            help="Sube un archivo Excel que contenga la hoja 'Hoja1' estructurada según el estándar AMATERRA.",
        )
        if uploaded_file is not None:
            uploaded_bytes = uploaded_file.read()
            st.sidebar.success(f"Archivo subido: {uploaded_file.name}")
        else:
            st.sidebar.info("Utilizando dataset predeterminado mientras no se cargue un archivo.")

    # Cargar y validar DataFrame limpio
    try:
        df = get_cached_dataset(uploaded_bytes)
        processor = AgrarianDataProcessor(df)
        macro_kpis = processor.get_macro_kpis()
    except Exception as e:
        st.error(f"Error crítico al procesar los datos: {e}")
        st.stop()

    # --- PERSONALIZACIÓN VISUAL ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Personalización Visual")
    palette_choice = st.sidebar.selectbox(
        "Paleta de Género",
        list(PALETTES.keys()),
        index=0,
        format_func=lambda k: PALETTES[k]["name"],
    )
    active_palette = PALETTES[palette_choice]

    # --- PARÁMETROS ANALÍTICOS ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Parámetros Analíticos")

    age_mode_radio = st.sidebar.radio(
        "Tramos de Edad",
        ["4 Tramos (Estándar)", "3 Tramos (Compacto 18-40, 41-55, >55)"],
        index=0,
    )
    age_mode_param = "4_tramos" if "4" in age_mode_radio else "3_tramos"

    surface_mode_radio = st.sidebar.radio(
        "Estratos de Superficie",
        ["Agronómico (<=5, 5-20, 20-50, >50 ha)", "Clásico (<2, 2-5, 5-10, >10 ha)"],
        index=0,
    )
    surface_mode_param = "agronomico" if "Agronómico" in surface_mode_radio else "clasico"

    # --- MÓDULO DE EXPORTACIÓN DIRECTA (ACCIÓN DE 1 CLIC) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Exportación Ejecutiva")
    st.sidebar.caption("Genera la presentación PowerPoint editable y el reporte consolidado en Excel.")

    export_btn = st.sidebar.button(
        "📥 Generar Presentación PPTX y Reporte Excel",
        type="primary",
        use_container_width=True,
    )

    pptx_path = Path("exports/presentacion_agraria_bizkaia.pptx")
    excel_path = Path("exports/tables/tablas_resumen.xlsx")

    if export_btn:
        with st.sidebar.status("Ejecutando exportación ejecutiva...", expanded=True) as status:
            st.write("1/3 Renderizando figuras a 300 DPI con Kaleido...")
            fig_s = build_sankey_overview(macro_kpis, color_h=active_palette["hombre"], color_m=active_palette["mujer"])
            fig_p = build_age_pyramid_divergent(processor.get_age_distribution("ALL", age_mode_param), colors=active_palette)
            fig_d = build_dumbbell_economic_gap(macro_kpis, metric="both", colors=active_palette)
            fig_sub = build_subsectors_horizontal_bar(processor.get_subsectors_summary("ALL"), top_n=12, colors=active_palette)
            fig_t = build_territorial_ranking(processor.get_territorial_summary("ALL"), colors=active_palette)

            chart_paths = {
                "sankey": export_chart(fig_s, "01_macro_embudo")["png"],
                "pyramid": export_chart(fig_p, "02_piramide_demografica")["png"],
                "dumbbell": export_chart(fig_d, "03_mancuerna_brechas")["png"],
                "subsectors": export_chart(fig_sub, "04_subsectores_ote")["png"],
                "territory": export_chart(fig_t, "05_ranking_territorial")["png"],
            }

            st.write("2/3 Creando libro consolidado con openpyxl...")
            tables_export = {
                "Demografia Edad": processor.get_age_distribution("ALL", age_mode_param),
                "Estratos Superficie": processor.get_surface_strata("ALL", surface_mode_param),
                "Subsectores OTE UE": processor.get_subsectors_summary("ALL"),
                "Formas Juridicas": processor.get_legal_status_summary("ALL"),
                "Ranking Territorial": processor.get_territorial_summary("ALL"),
                "Sostenibilidad Eco": processor.get_sustainability_summary("ALL"),
            }
            export_tables_to_excel(tables_export, output_filepath=str(excel_path))

            st.write("3/3 Construyendo presentación PowerPoint (16:9)...")
            builder = PowerPointReportBuilder(
                title="Estudio de Explotaciones Agrarias Comerciales de Bizkaia: Brecha de Género y Dimensión Productiva",
                author="Plataforma Analítica AMATERRA Mujeres",
            )
            builder.build_full_report(
                kpis=macro_kpis,
                df_age=processor.get_age_distribution("ALL", age_mode_param),
                df_sub=processor.get_subsectors_summary("ALL"),
                df_legal=processor.get_legal_status_summary("ALL"),
                df_terr=processor.get_territorial_summary("ALL"),
                chart_paths=chart_paths,
                output_filepath=str(pptx_path),
            )
            status.update(label="¡Archivos generados en /exports/!", state="complete", expanded=False)

    # Botones de descarga directa si los archivos existen
    if pptx_path.exists():
        with open(pptx_path, "rb") as f_pptx:
            st.sidebar.download_button(
                label="📊 presentacion_agraria_bizkaia.pptx",
                data=f_pptx.read(),
                file_name="presentacion_agraria_bizkaia.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
            )

    if excel_path.exists():
        with open(excel_path, "rb") as f_xls:
            st.sidebar.download_button(
                label="📗 tablas_resumen.xlsx",
                data=f_xls.read(),
                file_name="tablas_resumen.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    # ==========================================================================
    # 3. CUERPO PRINCIPAL (NARRATIVA "MACRO A MICRO")
    # ==========================================================================

    # --- CABECERA Y KPIS MACRO (NIVEL 0) ---
    st.title("🌾 Bizkaia Agraria | Brecha de Género")
    st.caption(
        "Diagnóstico analítico exhaustivo del sector agrario de mercado de Bizkaia. "
        "Se excluye el autoconsumo de subsistencia y se analiza el **universo comercial: 3.323 explotaciones**."
    )

    # Fila con 4 columnas de métricas ejecutivas
    atp_kpis = macro_kpis.get("atp", {})
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-label">Explotaciones de Mercado</div>
                <div class="metric-val">{macro_kpis['total_comerciales']:,}</div>
                <div class="metric-sub">ATP (Prioritaria): {macro_kpis['total_atp']:,} | No ATP: {macro_kpis['total_no_atp']:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-container metric-container-purple">
                <div class="metric-label">Tasa de Feminización</div>
                <div class="metric-val">{macro_kpis['pct_feminizacion_global']:.1f}%</div>
                <div class="metric-sub">{macro_kpis['total_mujeres']:,} Mujeres vs {macro_kpis['total_hombres']:,} Hombres (56 M por 100 H)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-container metric-container-red">
                <div class="metric-label">Brecha Media en Superficie</div>
                <div class="metric-val">-{atp_kpis.get('brecha_superficie_pct', 25.5):.1f}%</div>
                <div class="metric-sub">ATP: {atp_kpis.get('superficie_media_hombres', 32.6):.1f} ha (H) vs {atp_kpis.get('superficie_media_mujeres', 24.2):.1f} ha (M)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-container metric-container-red">
                <div class="metric-label">Brecha Media en UTAs (Empleo)</div>
                <div class="metric-val">-{atp_kpis.get('brecha_utas_pct', 32.4):.1f}%</div>
                <div class="metric-sub">ATP: {atp_kpis.get('utas_media_hombres', 2.10):.2f} (H) vs {atp_kpis.get('utas_media_mujeres', 1.42):.2f} UTAs (M)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- PESTAÑAS DE NAVEGACIÓN TEMÁTICA ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Estructura Macro (El Embudo)",
        "👥 Demografía y Relevo Generacional",
        "🚜 Dimensión Física y Empleo (ha y UTAs)",
        "🌱 Sostenibilidad y Transición Verde",
        "🔍 Zoom Sectorial, Jurídico y Territorial (Micro)",
    ])

    # --------------------------------------------------------------------------
    # TAB 1: ESTRUCTURA MACRO (EL EMBUDO)
    # --------------------------------------------------------------------------
    with tab1:
        st.subheader("Nivel 1: El Macro-Embudo de la Comercialización Agraria")
        st.caption("Flujo de representatividad desde el censo comercial global hasta los segmentos de profesionalidad.")

        fig_sankey = build_sankey_overview(
            macro_kpis,
            color_h=active_palette["hombre"],
            color_m=active_palette["mujer"],
            height=480,
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

        st.info(
            "💡 **Paridad Relativa en la Representatividad (35,9%):** "
            "La tasa de feminización se mantiene exactamente idéntica tanto en el segmento profesional prioritario "
            "(ATP: 35,9%, 190 mujeres de 529 titulares) como en el complementario no prioritario (No ATP: 35,9%, 1.004 mujeres de 2.794 titulares). "
            "Sin embargo, el **84,1%** de todas las explotaciones comerciales de Bizkaia corresponden al segmento No ATP."
        )

        with st.expander("Ver tabla comparativa Macro (Fines de mercado: ATP vs No ATP)"):
            atp = macro_kpis.get("atp", {})
            no_atp = macro_kpis.get("no_atp", {})
            df_macro_table = pd.DataFrame([
                {"Segmento": "ATP (Profesional Prioritaria)", "Hombres": atp.get("hombres", 339), "Mujeres": atp.get("mujeres", 190), "Total Explotaciones": atp.get("total", 529), "% Feminización": f"{atp.get('pct_feminizacion', 35.9):.1f}%"},
                {"Segmento": "No ATP (Agrícola Complementaria)", "Hombres": no_atp.get("hombres", 1790), "Mujeres": no_atp.get("mujeres", 1004), "Total Explotaciones": no_atp.get("total", 2794), "% Feminización": f"{no_atp.get('pct_feminizacion', 35.9):.1f}%"},
                {"Segmento": "Total Comercial de Mercado", "Hombres": macro_kpis.get("total_hombres", 2129), "Mujeres": macro_kpis.get("total_mujeres", 1194), "Total Explotaciones": macro_kpis.get("total_comerciales", 3323), "% Feminización": f"{macro_kpis.get('pct_feminizacion_global', 35.9):.1f}%"},
            ])
            st.dataframe(df_macro_table, use_container_width=True, hide_index=True)
            st.download_button(
                "📥 Descargar balance Macro (CSV)",
                df_macro_table.to_csv(index=False).encode("utf-8"),
                "balance_macro_agrario_bizkaia.csv",
                "text/csv",
            )

    # --------------------------------------------------------------------------
    # TAB 2: DEMOGRAFÍA Y RELEVO GENERACIONAL
    # --------------------------------------------------------------------------
    with tab2:
        st.subheader("Nivel 2: Pirámide Demográfica y Relevo Generacional")
        
        col_seg_t2, _ = st.columns([2, 3])
        with col_seg_t2:
            seg_demog = st.selectbox(
                "Segmento a analizar:",
                ["Comparativa Ambos", "Solo ATP", "Solo No ATP"],
                index=0,
                key="seg_demog_select",
            )

        segment_arg = "ALL" if "Ambos" in seg_demog else ("ATP" if "Solo ATP" in seg_demog else "No ATP")
        df_age = processor.get_age_distribution(segment=segment_arg, mode=age_mode_param)

        fig_pyramid = build_age_pyramid_divergent(
            df_age,
            colors=active_palette,
            title=f"Estructura Demográfica por Edad y Género — Segmento: {seg_demog}",
            subtitle="Hombres (izquierda) vs Mujeres (derecha) con la tasa de feminización por tramo",
            height=460,
        )
        st.plotly_chart(fig_pyramid, use_container_width=True)

        st.warning(
            "⚠️ **Alerta Crítica de Titularidad Tardía:** "
            "El **56,1% de las mujeres** en agricultura no profesional (No ATP) supera los **65 años**. "
            "En toda Bizkaia únicamente existen **85 mujeres menores de 41 años** al frente de una explotación comercial, "
            "evidenciando un severo cuello de botella en el relevo generacional y un alto riesgo de abandono de tierras en la próxima década."
        )

        with st.expander("Ver tabla demográfica interactiva con recuentos y porcentajes"):
            st.dataframe(df_age, use_container_width=True, hide_index=True)
            st.download_button(
                "📥 Descargar datos de edad (CSV)",
                df_age.to_csv(index=False).encode("utf-8"),
                f"demografia_edad_{segment_arg.lower()}.csv",
                "text/csv",
            )

    # --------------------------------------------------------------------------
    # TAB 3: DIMENSIÓN FÍSICA Y EMPLEO (HA Y UTAS)
    # --------------------------------------------------------------------------
    with tab3:
        st.subheader("Nivel 2: Dimensión Física y Empleo (ha y UTAs)")
        st.caption("Comparativa de superficie media y capacidad laboral (UTAs) con brechas de género calculadas.")

        # Selector de métrica para el Dumbbell
        col_m1, _ = st.columns([2, 3])
        with col_m1:
            metric_dumbbell = st.radio(
                "Visualizar Brechas en Gráfico Dumbbell:",
                ["Ambas Métricas (Superficie y UTAs)", "Solo Superficie (ha)", "Solo Empleo (UTAs)"],
                index=0,
                horizontal=True,
            )
        d_mode = "both" if "Ambas" in metric_dumbbell else ("superficie" if "Superficie" in metric_dumbbell else "utas")

        fig_dumbbell = build_dumbbell_economic_gap(
            macro_kpis,
            metric=d_mode,
            colors=active_palette,
            height=400,
        )
        st.plotly_chart(fig_dumbbell, use_container_width=True)

        # Tabla cruzada de hectáreas y UTAs medias con porcentajes de brecha calculados
        st.markdown("#### Tabla Cruzada: Medias de Superficie, UTAs y Brecha de Género")
        df_brechas = pd.DataFrame([
            {
                "Segmento": "ATP (Profesional Prioritaria)",
                "Sup. Media H (ha)": f"{macro_kpis['atp']['superficie_media_hombres']:.2f} ha",
                "Sup. Media M (ha)": f"{macro_kpis['atp']['superficie_media_mujeres']:.2f} ha",
                "Brecha Superficie (%)": f"-{macro_kpis['atp']['brecha_superficie_pct']:.1f}%",
                "UTAs Media H": f"{macro_kpis['atp']['utas_media_hombres']:.2f}",
                "UTAs Media M": f"{macro_kpis['atp']['utas_media_mujeres']:.2f}",
                "Brecha UTAs (%)": f"-{macro_kpis['atp']['brecha_utas_pct']:.1f}%",
            },
            {
                "Segmento": "No ATP (Agrícola Complementaria)",
                "Sup. Media H (ha)": f"{macro_kpis['no_atp']['superficie_media_hombres']:.2f} ha",
                "Sup. Media M (ha)": f"{macro_kpis['no_atp']['superficie_media_mujeres']:.2f} ha",
                "Brecha Superficie (%)": f"-{macro_kpis['no_atp']['brecha_superficie_pct']:.1f}%",
                "UTAs Media H": f"{macro_kpis['no_atp']['utas_media_hombres']:.2f}",
                "UTAs Media M": f"{macro_kpis['no_atp']['utas_media_mujeres']:.2f}",
                "Brecha UTAs (%)": f"-{macro_kpis['no_atp']['brecha_utas_pct']:.1f}%",
            },
            {
                "Segmento": "Total Comercial de Mercado",
                "Sup. Media H (ha)": f"{macro_kpis['global']['superficie_media_hombres']:.2f} ha",
                "Sup. Media M (ha)": f"{macro_kpis['global']['superficie_media_mujeres']:.2f} ha",
                "Brecha Superficie (%)": f"-{macro_kpis['global']['brecha_superficie_pct']:.1f}%",
                "UTAs Media H": f"{macro_kpis['global']['utas_media_hombres']:.2f}",
                "UTAs Media M": f"{macro_kpis['global']['utas_media_mujeres']:.2f}",
                "Brecha UTAs (%)": f"-{macro_kpis['global']['brecha_utas_pct']:.1f}%",
            },
        ])
        st.dataframe(df_brechas, use_container_width=True, hide_index=True)

        # Distribución de Explotaciones por Estrato de Superficie
        st.markdown("---")
        st.markdown("#### Distribución de Explotaciones por Estrato de Superficie")
        
        col_surf_s, _ = st.columns([2, 3])
        with col_surf_s:
            seg_surf = st.selectbox(
                "Segmento para análisis de estratos de superficie:",
                ["Comparativa Ambos", "Solo ATP", "Solo No ATP"],
                index=0,
                key="seg_surf_select",
            )
        seg_surf_arg = "ALL" if "Ambos" in seg_surf else ("ATP" if "Solo ATP" in seg_surf else "No ATP")
        df_surf = processor.get_surface_strata(segment=seg_surf_arg, strata_type=surface_mode_param)

        fig_surf = go.Figure()
        fig_surf.add_trace(
            go.Bar(
                y=df_surf["Estrato"],
                x=df_surf["Hombres"],
                name="Hombres",
                orientation="h",
                marker_color=active_palette["hombre"],
                text=[f"{h:,}" for h in df_surf["Hombres"]],
                textposition="inside",
            )
        )
        fig_surf.add_trace(
            go.Bar(
                y=df_surf["Estrato"],
                x=df_surf["Mujeres"],
                name="Mujeres",
                orientation="h",
                marker_color=active_palette["mujer"],
                text=[f"{m:,} ({p:.1f}%)" for m, p in zip(df_surf["Mujeres"], df_surf["% Feminización"])],
                textposition="inside",
            )
        )
        fig_surf.update_layout(
            barmode="stack",
            height=360,
            xaxis=dict(title="Número de Explotaciones", gridcolor="#F0F2F5"),
            yaxis=dict(title=""),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig_surf, use_container_width=True)

        with st.expander("Ver desglose cuantitativo por estratos de superficie"):
            st.dataframe(df_surf, use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TAB 4: SOSTENIBILIDAD Y TRANSICIÓN VERDE
    # --------------------------------------------------------------------------
    with tab4:
        st.subheader("Nivel 2: Sostenibilidad y Transición Verde")
        st.caption("Adopción de prácticas ecológicas y agroambientales según titularidad de género.")

        col_seg_eco, _ = st.columns([2, 3])
        with col_seg_eco:
            seg_eco = st.selectbox(
                "Segmento a visualizar:",
                ["Comparativa Ambos", "Solo ATP (Profesional)", "Solo No ATP"],
                index=0,
                key="seg_eco_select",
            )
        seg_eco_arg = "ALL" if "Ambos" in seg_eco else ("ATP" if "Solo ATP" in seg_eco else "No ATP")
        df_eco = processor.get_sustainability_summary(seg_eco_arg)

        fig_eco = build_sustainability_breakdown(
            df_eco,
            colors=active_palette,
            title=f"Explotaciones Ecológicas vs Convencionales — {seg_eco}",
            height=400,
        )
        st.plotly_chart(fig_eco, use_container_width=True)

        st.success(
            "🌱 **Liderazgo Femenino en Agroecología Profesional:** "
            "En el sector profesional (ATP), las mujeres lideran la tasa relativa con una cuota del **39,1%** en explotaciones ecológicas "
            "(18 de 46 explotaciones certificadas o en proceso de conversión), superando la tasa de feminización agraria global (35,9%). "
            "Las titulares demuestran mayor proactividad hacia modelos productivos sostenibles y de valor añadido."
        )

        with st.expander("Ver tabla de datos ecológicos"):
            st.dataframe(df_eco, use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # TAB 5: ZOOM SECTORIAL, JURÍDICO Y TERRITORIAL (MICRO)
    # --------------------------------------------------------------------------
    with tab5:
        st.subheader("Nivel 3 y 4: Zoom Sectorial, Jurídico y Territorial (Micro)")

        col_f1, col_f2 = st.columns([2, 3])
        with col_f1:
            seg_micro = st.selectbox(
                "Selector de Subsegmento:",
                ["Solo ATP", "Solo No ATP", "Comparativa Ambos"],
                index=0,
                key="seg_micro_select",
            )
        with col_f2:
            top_n_sub = st.slider("Top N de subsectores a visualizar:", min_value=5, max_value=20, value=12)

        seg_micro_arg = "ATP" if seg_micro == "Solo ATP" else ("No ATP" if seg_micro == "Solo No ATP" else "ALL")
        df_sub_micro = processor.get_subsectors_summary(segment=seg_micro_arg)
        df_legal_micro = processor.get_legal_status_summary(segment=seg_micro_arg)

        # Gráficos en dos columnas: Subsectores OTE y Formas Jurídicas
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_sub = build_subsectors_horizontal_bar(
                df_sub_micro,
                top_n=top_n_sub,
                colors=active_palette,
                title=f"Subsectores OTE UE (Top {top_n_sub}) — {seg_micro}",
                height=520,
            )
            st.plotly_chart(fig_sub, use_container_width=True)

        with col_g2:
            fig_legal = build_legal_status_bar(
                df_legal_micro,
                colors=active_palette,
                title=f"Formas Jurídicas — {seg_micro}",
                height=520,
            )
            st.plotly_chart(fig_legal, use_container_width=True)

        st.warning(
            "🏛️ **Invisibilidad Jurídica y Escasez de Titularidad Compartida (Ley 35/2011):** "
            "En todo el censo comercial de Bizkaia apenas se registran **10 explotaciones (0,3%)** bajo la figura de Titularidad Compartida. "
            "El **98,3% (3.266 explotaciones)** están catalogadas como Persona Física individual, lo que invisibiliza formalmente "
            "la corresponsabilidad y la participación económica y societaria de las mujeres."
        )

        st.markdown("---")
        st.markdown("#### Ranking Territorial de Feminización Agraria")

        col_terr_sel, _ = st.columns([2, 3])
        with col_terr_sel:
            terr_level = st.radio(
                "Desglose Territorial:",
                ["Oficina Comarcal Agraria (OCA)", "Comarca (Asociación Desarrollo Rural - ADR)"],
                index=0,
                horizontal=True,
            )
        by_param = "OCA" if "OCA" in terr_level else "COMARCA"
        df_terr_micro = processor.get_territorial_summary(segment=seg_micro_arg, by=by_param)

        fig_terr = build_territorial_ranking(
            df_terr_micro,
            colors=active_palette,
            title=f"Ranking por {by_param} — Razón de Feminización ({seg_micro})",
            subtitle="Mujeres por cada 100 hombres comparadas contra el promedio de referencia",
            height=460,
        )
        st.plotly_chart(fig_terr, use_container_width=True)

        with st.expander(f"Ver datos cuantitativos por {by_param}"):
            st.dataframe(df_terr_micro, use_container_width=True, hide_index=True)
            st.download_button(
                f"📥 Descargar balance territorial ({by_param})",
                df_terr_micro.to_csv(index=False).encode("utf-8"),
                f"ranking_territorial_{by_param.lower()}_{seg_micro_arg.lower()}.csv",
                "text/csv",
            )


if __name__ == "__main__":
    main()
