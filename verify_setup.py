"""Script de verificación integral del entorno y estructura de proyecto.

Comprueba:
1. Instalación y versiones de dependencias en el entorno virtual.
2. Accesibilidad e integridad del fichero Excel en la raíz.
3. Ejecución del pipeline ETL en src.data_processor (Hoja1, mapeo comarcas, tramos).
4. Generación de gráficos en src.visualizer (Sankey, pirámides, barras).
5. Motor de exportación en src.exporter (PPTX, imágenes 300 dpi en charts/, tablas en tables/).
"""

import sys
from pathlib import Path

# Colores ANSI para terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def report(test_name: str, passed: bool, detail: str = ""):
    status = f"{GREEN}[PASS]{RESET}" if passed else f"{RED}[FAIL]{RESET}"
    print(f"{status} {test_name:<45} {detail}")
    if not passed:
        sys.exit(1)


def main():
    print(f"\n{BLUE}=== INICIANDO VERIFICACIÓN DE ENTORNO Y ARQUITECTURA AMATERRA ==={RESET}\n")

    # 1. Comprobar intérprete y dependencias
    required_packages = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("plotly", "plotly"),
        ("python-pptx", "pptx"),
        ("kaleido", "kaleido"),
        ("numpy", "numpy"),
    ]

    for pkg_name, import_mod in required_packages:
        try:
            mod = __import__(import_mod)
            version = getattr(mod, "__version__", "instalado")
            report(f"Dependencia: {pkg_name}", True, f"v{version}")
        except ImportError as e:
            report(f"Dependencia: {pkg_name}", False, f"Error: {e}")

    # 2. Comprobar fichero fuente Excel en raíz
    root_dir = Path(__file__).resolve().parent
    excel_path = root_dir / "AMATERRA_Mujeres_DatosExplotacionesAlta_Datos01.xlsx"

    if excel_path.exists():
        size_mb = round(excel_path.stat().st_size / (1024 * 1024), 2)
        report("Fichero Excel en raíz", True, f"{excel_path.name} ({size_mb} MB)")
    else:
        report("Fichero Excel en raíz", False, f"No encontrado en {excel_path}")

    # 3. Comprobar estructura de carpetas
    for folder in ["src", "exports/charts", "exports/tables"]:
        f_path = root_dir / folder
        report(f"Directorio: {folder}", f_path.is_dir(), f"{f_path.relative_to(root_dir)}")

    # 4. Pipeline ETL y Data Processor
    try:
        from src.data_processor import load_and_process_data, get_kpis_summary
        from src.config import OCA_TO_COMARCA

        df = load_and_process_data(excel_path)
        kpis = get_kpis_summary(df)

        has_comarca = "COMARCA" in df.columns
        has_genero = "GENERO" in df.columns
        has_edad_4 = "TRAMO_EDAD_4" in df.columns
        has_sup = "TRAMO_SUPERFICIE" in df.columns

        etl_ok = has_comarca and has_genero and has_edad_4 and has_sup and len(df) > 0
        detail = (
            f"{len(df):,} filas procesadas | "
            f"{kpis['total_mujeres']} mujeres ({kpis['porcentaje_mujeres']}%) | "
            f"{len(df['COMARCA'].unique())} comarcas identificadas"
        )
        report("Pipeline ETL (src/data_processor.py)", etl_ok, detail)

    except Exception as e:
        report("Pipeline ETL (src/data_processor.py)", False, f"Excepción: {e}")

    # 5. Generación de Gráficos (Visualizer)
    try:
        from src.visualizer import (
            create_demographic_pyramid,
            create_sankey_flow,
            create_comarca_breakdown_chart,
        )

        fig_pyramid = create_demographic_pyramid(df)
        fig_sankey = create_sankey_flow(df)
        fig_comarca = create_comarca_breakdown_chart(df)

        charts_ok = fig_pyramid is not None and fig_sankey is not None and fig_comarca is not None
        report("Motor Visual Plotly (Sankey, Pirámide, Barras)", charts_ok, "Figuras creadas correctamente")

    except Exception as e:
        report("Motor Visual Plotly (Visualizer)", False, f"Excepción: {e}")

    # 6. Motor de Exportación (PPTX, 300 dpi, tablas)
    try:
        from src.exporter import (
            PresentationReport,
            export_chart_to_file,
            export_consolidated_tables,
        )

        # Prueba de exportación de tabla
        t_path = export_consolidated_tables({"Muestra": df.head(10)}, filename="test_check.xlsx")
        report("Exportación de Tablas (.xlsx)", t_path.exists(), f"Generado en {t_path.name}")
        t_path.unlink(missing_ok=True)

        # Prueba de exportación de gráfico 300 dpi
        c_path = export_chart_to_file(fig_comarca, "test_check.png", dpi=300)
        report("Exportación de Gráfico (300 DPI)", c_path.exists(), f"Generado en {c_path.name}")
        c_path.unlink(missing_ok=True)

        # Prueba de PowerPoint
        ppt = PresentationReport(title="Test Suite PPTX")
        ppt.add_kpis_slide("KPIs Test", {"Total": kpis["total_explotaciones"]})
        ppt.add_chart_slide("Comarcas Test", fig_comarca)
        p_path = ppt.save("test_check.pptx")
        report("Motor PPTX (python-pptx + Kaleido)", p_path.exists(), f"Generado en {p_path.name}")
        p_path.unlink(missing_ok=True)

    except Exception as e:
        report("Motor de Exportación (src/exporter.py)", False, f"Excepción: {e}")

    print(f"\n{GREEN}=== TODAS LAS PRUEBAS DE VERIFICACIÓN SE HAN SUPERADO CON ÉXITO ==={RESET}\n")


if __name__ == "__main__":
    main()
