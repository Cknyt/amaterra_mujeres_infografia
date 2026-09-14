"""Módulo central de procesamiento analítico y ETL (src/data_processor.py).

Única fuente de verdad analítica del proyecto AMATERRA:
- Lee exclusivamente Hoja1 del fichero Excel oficial.
- Limpia y normaliza campos clave (ATP, Sexo, OCA, Ecológico, Condición Jurídica, OTE).
- Aplica el filtrado crítico de mercado (TIPO ACTIVIDAD == 'FINES DE MERCADO') y paridad binaria de sexo.
- Provee la clase AgrarianDataProcessor con métodos estructurados para KPIs, demografía,
  superficies, subsectores, personalidad jurídica, comarcas y sostenibilidad.
- Incorpora batería de aserciones de negocio ejecutables directamente vía CLI.
"""

from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Asegurar que el directorio raíz esté en sys.path al ejecutar directamente como script
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd

from src.config import (
    AGE_BRACKETS_3,
    AGE_BRACKETS_4,
    DEFAULT_EXCEL_PATH,
    OCA_TO_COMARCA,
    SURFACE_BRACKETS_AGRONOMICO,
    SURFACE_BRACKETS_CLASICO,
)

# Asegurar codificación utf-8 para la salida estándar en terminales Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _clean_column_names(columns: List[Any]) -> List[str]:
    """Sanea nombres de columnas con caracteres de reemplazo unicode (\ufffd) o espacios."""
    cleaned = []
    for c in columns:
        s = str(c).strip()
        s = s.replace("\ufffdN", "ÓN").replace("\ufffdDICA", "ÍDICA").replace("\ufffd", "Ó")
        cleaned.append(s)
    return cleaned


def _classify_bracket(val: float, brackets: List[Tuple[float, float, str]]) -> str:
    """Clasifica un valor numérico según una lista ordenada de intervalos (min, max, label)."""
    if pd.isna(val):
        return "No consta"
    try:
        n = float(val)
    except (ValueError, TypeError):
        return "No consta"

    for min_v, max_v, label in brackets:
        if min_v <= n <= max_v:
            return label
    return "No consta"


def _classify_eco_status(val: Any) -> Tuple[bool, str]:
    """Detecta si una explotación es ecológica (IS_ECO) y categoriza su TIPO_ECO."""
    if pd.isna(val):
        return False, "Convencional"
    s = str(val).strip().lower()
    if not s or s == "nan":
        return False, "Convencional"

    # En proceso de conversión
    if "convers" in s or "en proceso" in s:
        return True, "En proceso"
    # Certificado
    if "certifi" in s:
        return True, "Certificado"
    # Otros textos descriptivos ecológicos
    return False, "Mixto/Otros"


def load_and_clean_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Carga y procesa exclusivamente Hoja1 de datos agrarios de mercado.

    Args:
        filepath: Ruta al archivo Excel. Si es None, utiliza DEFAULT_EXCEL_PATH.

    Returns:
        pd.DataFrame limpio con 3.323 explotaciones comerciales (2.129 hombres, 1.194 mujeres).
    """
    if filepath is None:
        target = DEFAULT_EXCEL_PATH
        if not target.exists():
            raise FileNotFoundError(f"No se encontró el fichero de datos en: {target.resolve()}")
    elif isinstance(filepath, (str, Path)):
        target = Path(filepath)
        if not target.exists():
            raise FileNotFoundError(f"No se encontró el fichero de datos en: {target.resolve()}")
    else:
        # Permite cargar directamente buffers en memoria como UploadedFile de Streamlit o BytesIO
        target = filepath

    # 1. Cargar Hoja1 usando pandas y openpyxl
    df = pd.read_excel(target, sheet_name="Hoja1", engine="openpyxl")

    # Saneamiento de nombres de columnas
    df.columns = _clean_column_names(df.columns)

    # 2. Limpieza básica de strings (eliminar espacios en blanco en columnas clave)
    key_str_cols = [
        "TIPO ACTIVIDAD",
        "CALIFICACION ATP",
        "SEXO",
        "OCA",
        "CONDICIÓN JURÍDICA",
        "DESCRIPCIÓN OTE UE",
    ]
    for col in key_str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 3. FILTRADO CRÍTICO DE MERCADO:
    # - Exclusivamente TIPO ACTIVIDAD == 'FINES DE MERCADO'
    df = df[df["TIPO ACTIVIDAD"] == "FINES DE MERCADO"].copy()

    # - Descartar registros donde SEXO no sea 'hombre' ni 'mujer'
    df["SEXO"] = df["SEXO"].str.lower()
    df = df[df["SEXO"].isin(["hombre", "mujer"])].copy()

    # 4. Normalización de valores booleanos y categorías:
    # CALIFICACION ATP: ['Bai/Si', 'Si', 'SI', 'BAI/SI'] -> 'ATP'; ['Ez/No', 'No', 'NO', 'EZ/NO'] -> 'No ATP'
    atp_normalized_map = {
        "bai/si": "ATP",
        "si": "ATP",
        "ez/no": "No ATP",
        "no": "No ATP",
    }
    df["CALIFICACION ATP"] = df["CALIFICACION ATP"].str.lower().map(atp_normalized_map).fillna("No ATP")

    # Mapeo OCA a COMARCA
    df["OCA"] = df["OCA"].str.upper()
    df["COMARCA"] = df["OCA"].map(OCA_TO_COMARCA).fillna("OTRA")

    # Detección de explotaciones ecológicas
    eco_results = df["ECOLOGICO"].apply(_classify_eco_status)
    df["IS_ECO"] = [r[0] for r in eco_results]
    df["TIPO_ECO"] = [r[1] for r in eco_results]

    # Conversión numérica de variables métricas
    df["SUPERFICIE_NUM"] = pd.to_numeric(df["SUPERFICIE"], errors="coerce").fillna(0.0)
    df["UTAS_NUM"] = pd.to_numeric(df["UTAS FINALES"], errors="coerce").fillna(0.0)
    df["EDAD_NUM"] = pd.to_numeric(df["EDAD"], errors="coerce")

    # Segmentación precalculada por tramos
    df["TRAMO_EDAD_4"] = df["EDAD_NUM"].apply(lambda v: _classify_bracket(v, AGE_BRACKETS_4))
    df["TRAMO_EDAD_3"] = df["EDAD_NUM"].apply(lambda v: _classify_bracket(v, AGE_BRACKETS_3))
    df["ESTRATO_AGRONOMICO"] = df["SUPERFICIE_NUM"].apply(lambda v: _classify_bracket(v, SURFACE_BRACKETS_AGRONOMICO))
    df["ESTRATO_CLASICO"] = df["SUPERFICIE_NUM"].apply(lambda v: _classify_bracket(v, SURFACE_BRACKETS_CLASICO))

    # Variable de visualización con mayúscula inicial
    df["GENERO"] = df["SEXO"].map({"hombre": "Hombre", "mujer": "Mujer"})
    df["TRAMO_SUPERFICIE"] = df["ESTRATO_AGRONOMICO"]

    return df


# Alias de compatibilidad
load_and_process_data = load_and_clean_data


def get_kpis_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Helper de compatibilidad que retorna resumen ejecutivo simple para la cabecera del dashboard."""
    total = len(df)
    mujeres_count = int((df["SEXO"] == "mujer").sum())
    hombres_count = int((df["SEXO"] == "hombre").sum())
    pct_mujeres = round((mujeres_count / total * 100), 1) if total > 0 else 0.0

    sup_total = round(float(df["SUPERFICIE_NUM"].sum()), 2)
    sup_media = round(float(df["SUPERFICIE_NUM"].mean()), 2) if total > 0 else 0.0
    edad_media = round(float(df["EDAD_NUM"].dropna().mean()), 1) if not df["EDAD_NUM"].dropna().empty else 0.0

    return {
        "total_explotaciones": total,
        "total_mujeres": mujeres_count,
        "total_hombres": hombres_count,
        "porcentaje_mujeres": pct_mujeres,
        "superficie_total_ha": sup_total,
        "superficie_media_ha": sup_media,
        "edad_media": edad_media,
    }


def apply_filters(
    df: pd.DataFrame,
    comarcas: Optional[List[str]] = None,
    generos: Optional[List[str]] = None,
    tramos_edad: Optional[List[str]] = None,
    tramos_superficie: Optional[List[str]] = None,
    segmento_atp: Optional[str] = None,
) -> pd.DataFrame:
    """Aplica filtros multidimensionales sobre el DataFrame procesado."""
    filtered = df.copy()

    if comarcas:
        filtered = filtered[filtered["COMARCA"].isin(comarcas)]
    if generos:
        filtered = filtered[filtered["GENERO"].isin(generos)]
    if tramos_edad:
        filtered = filtered[filtered["TRAMO_EDAD_4"].isin(tramos_edad)]
    if tramos_superficie:
        filtered = filtered[filtered["ESTRATO_AGRONOMICO"].isin(tramos_superficie)]
    if segmento_atp and segmento_atp != "Todos":
        filtered = filtered[filtered["CALIFICACION ATP"] == segmento_atp]

    return filtered


class AgrarianDataProcessor:
    """Clase analítica con tipado estricto para cálculo y agregación de datos agrarios."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @classmethod
    def from_file(cls, filepath: Optional[Union[str, Path]] = None) -> "AgrarianDataProcessor":
        """Instancia la clase cargando y limpiando los datos desde archivo."""
        clean_df = load_and_clean_data(filepath)
        return cls(clean_df)

    def _filter_segment(self, segment: str = "ALL") -> pd.DataFrame:
        """Filtra el conjunto de datos por segmento: 'ALL', 'ATP' o 'No ATP'."""
        seg_upper = segment.strip().upper()
        if seg_upper == "ALL":
            return self.df
        elif seg_upper == "ATP":
            return self.df[self.df["CALIFICACION ATP"] == "ATP"]
        elif seg_upper in ["NO ATP", "NO_ATP"]:
            return self.df[self.df["CALIFICACION ATP"] == "No ATP"]
        else:
            raise ValueError(f"Segmento no reconocido: '{segment}'. Opciones válidas: 'ALL', 'ATP', 'No ATP'.")

    def get_macro_kpis(self) -> Dict[str, Any]:
        """Calcula los macro-indicadores cuantitativos globales y por segmento."""
        total = len(self.df)
        hombres = int((self.df["SEXO"] == "hombre").sum())
        mujeres = int((self.df["SEXO"] == "mujer").sum())
        pct_fem = round((mujeres / total * 100), 2) if total > 0 else 0.0

        atp_df = self.df[self.df["CALIFICACION ATP"] == "ATP"]
        no_atp_df = self.df[self.df["CALIFICACION ATP"] == "No ATP"]

        def _calc_segment_stats(sub_df: pd.DataFrame) -> Dict[str, float]:
            h_sub = sub_df[sub_df["SEXO"] == "hombre"]
            m_sub = sub_df[sub_df["SEXO"] == "mujer"]

            sup_h = float(h_sub["SUPERFICIE_NUM"].mean()) if not h_sub.empty else 0.0
            sup_m = float(m_sub["SUPERFICIE_NUM"].mean()) if not m_sub.empty else 0.0
            gap_sup = round(((sup_h - sup_m) / sup_h * 100), 2) if sup_h > 0 else 0.0

            utas_h = float(h_sub["UTAS_NUM"].mean()) if not h_sub.empty else 0.0
            utas_m = float(m_sub["UTAS_NUM"].mean()) if not m_sub.empty else 0.0
            gap_utas = round(((utas_h - utas_m) / utas_h * 100), 2) if utas_h > 0 else 0.0

            return {
                "total": len(sub_df),
                "hombres": len(h_sub),
                "mujeres": len(m_sub),
                "pct_feminizacion": round((len(m_sub) / max(1, len(sub_df)) * 100), 2),
                "superficie_media_hombres": round(sup_h, 2),
                "superficie_media_mujeres": round(sup_m, 2),
                "brecha_superficie_pct": gap_sup,
                "utas_media_hombres": round(utas_h, 2),
                "utas_media_mujeres": round(utas_m, 2),
                "brecha_utas_pct": gap_utas,
            }

        stats_atp = _calc_segment_stats(atp_df)
        stats_no_atp = _calc_segment_stats(no_atp_df)
        stats_global = _calc_segment_stats(self.df)

        return {
            "total_comerciales": total,
            "total_hombres": hombres,
            "total_mujeres": mujeres,
            "pct_feminizacion_global": pct_fem,
            "total_atp": len(atp_df),
            "total_no_atp": len(no_atp_df),
            "atp": stats_atp,
            "no_atp": stats_no_atp,
            "global": stats_global,
        }

    def get_age_distribution(self, segment: str = "ALL", mode: str = "4_tramos") -> pd.DataFrame:
        """Calcula la distribución demográfica por tramos de edad y género.

        Args:
            segment: 'ALL', 'ATP' o 'No ATP'.
            mode: '4_tramos' o '3_tramos'.

        Returns:
            pd.DataFrame con columnas: Tramo, Hombres, Mujeres, Total, % Feminización, Razón (M por 100 H).
        """
        data = self._filter_segment(segment)
        col_tramo = "TRAMO_EDAD_4" if mode == "4_tramos" else "TRAMO_EDAD_3"
        brackets = AGE_BRACKETS_4 if mode == "4_tramos" else AGE_BRACKETS_3
        order = [b[2] for b in brackets]

        ct = pd.crosstab(data[col_tramo], data["SEXO"]).reindex(order).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres

        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)
        razon_m_h = np.where(hombres > 0, np.round((mujeres / hombres) * 100, 1), 0.0)

        result = pd.DataFrame({
            "Tramo": ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
            "Razón (M por 100 H)": razon_m_h,
        })
        return result

    def get_surface_strata(self, segment: str = "ALL", strata_type: str = "agronomico") -> pd.DataFrame:
        """Calcula los recuentos y porcentajes de superficie cruzados por sexo.

        Args:
            segment: 'ALL', 'ATP' o 'No ATP'.
            strata_type: 'agronomico' o 'clasico'.

        Returns:
            pd.DataFrame con columnas: Estrato, Hombres, Mujeres, Total, % Feminización, % sobre Total.
        """
        data = self._filter_segment(segment)
        col_estrato = "ESTRATO_AGRONOMICO" if strata_type == "agronomico" else "ESTRATO_CLASICO"
        brackets = SURFACE_BRACKETS_AGRONOMICO if strata_type == "agronomico" else SURFACE_BRACKETS_CLASICO
        order = [b[2] for b in brackets]

        ct = pd.crosstab(data[col_estrato], data["SEXO"]).reindex(order).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres
        gran_total = max(1, len(data))

        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)
        pct_sobre_total = np.round((totales / gran_total) * 100, 1)

        result = pd.DataFrame({
            "Estrato": ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
            "% sobre Total": pct_sobre_total,
        })
        return result

    def get_subsectors_summary(self, segment: str = "ATP") -> pd.DataFrame:
        """Agrupa por orientación técnico-económica (DESCRIPCIÓN OTE UE) y sexo.

        Returns:
            pd.DataFrame ordenado con columnas: Subsector, Hombres, Mujeres, Total, % Feminización.
        """
        data = self._filter_segment(segment)
        ct = pd.crosstab(data["DESCRIPCIÓN OTE UE"], data["SEXO"]).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres
        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)

        result = pd.DataFrame({
            "Subsector": ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
        })
        return result.sort_values(by="Total", ascending=False).reset_index(drop=True)

    def get_legal_status_summary(self, segment: str = "ATP") -> pd.DataFrame:
        """Agrupa por CONDICIÓN JURÍDICA y sexo.

        Returns:
            pd.DataFrame con frecuencias y porcentajes.
        """
        data = self._filter_segment(segment)
        ct = pd.crosstab(data["CONDICIÓN JURÍDICA"], data["SEXO"]).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres
        gran_total = max(1, len(data))

        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)
        pct_sobre_total = np.round((totales / gran_total) * 100, 1)

        result = pd.DataFrame({
            "Condición Jurídica": ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
            "% sobre Total": pct_sobre_total,
        })
        return result.sort_values(by="Total", ascending=False).reset_index(drop=True)

    def get_territorial_summary(self, segment: str = "ATP", by: str = "COMARCA") -> pd.DataFrame:
        """Agrupa por Comarca calculada (COMARCA) u Oficina Comarcal Agraria (OCA).

        Args:
            segment: 'ALL', 'ATP' o 'No ATP'.
            by: 'COMARCA' u 'OCA'.

        Returns:
            pd.DataFrame con: Comarca/OCA, Hombres, Mujeres, Total, % Feminización, Razón (M por 100 H).
        """
        data = self._filter_segment(segment)
        group_col = "OCA" if str(by).upper() == "OCA" else "COMARCA"
        label_col = "OCA" if group_col == "OCA" else "Comarca"
        ct = pd.crosstab(data[group_col], data["SEXO"]).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres

        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)
        razon_m_h = np.where(hombres > 0, np.round((mujeres / hombres) * 100, 1), 0.0)

        result = pd.DataFrame({
            label_col: ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
            "Razón (M por 100 H)": razon_m_h,
        })
        return result.sort_values(by="Total", ascending=False).reset_index(drop=True)

    def get_sustainability_summary(self, segment: str = "ALL") -> pd.DataFrame:
        """Desglose por TIPO_ECO y sexo.

        Returns:
            pd.DataFrame con: Tipo Ecológico, Hombres, Mujeres, Total, % Feminización, % sobre Total.
        """
        data = self._filter_segment(segment)
        ct = pd.crosstab(data["TIPO_ECO"], data["SEXO"]).fillna(0).astype(int)

        if "hombre" not in ct.columns:
            ct["hombre"] = 0
        if "mujer" not in ct.columns:
            ct["mujer"] = 0

        hombres = ct["hombre"]
        mujeres = ct["mujer"]
        totales = hombres + mujeres
        gran_total = max(1, len(data))

        pct_fem = np.where(totales > 0, np.round((mujeres / totales) * 100, 1), 0.0)
        pct_sobre_total = np.round((totales / gran_total) * 100, 1)

        result = pd.DataFrame({
            "Tipo Ecológico": ct.index,
            "Hombres": hombres.values,
            "Mujeres": mujeres.values,
            "Total": totales.values,
            "% Feminización": pct_fem,
            "% sobre Total": pct_sobre_total,
        })
        return result.sort_values(by="Total", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    # --- BATERÍA DE VALIDACIÓN UNITARIA CONTRA REGLAS DE NEGOCIO ---
    print("Iniciando validación analítica de reglas de negocio...")

    df_clean = load_and_clean_data()
    processor = AgrarianDataProcessor(df_clean)

    # 1. Total registros y paridad
    assert len(df_clean) == 3323, f"Fallo: Total registros esperado 3323, obtenido {len(df_clean)}"
    assert (df_clean["SEXO"] == "hombre").sum() == 2129, "Fallo en recuento de hombres comercial"
    assert (df_clean["SEXO"] == "mujer").sum() == 1194, "Fallo en recuento de mujeres comercial"

    # 2. Segmentación ATP y No ATP
    atp_df = df_clean[df_clean["CALIFICACION ATP"] == "ATP"]
    no_atp_df = df_clean[df_clean["CALIFICACION ATP"] == "No ATP"]

    h_atp = int((atp_df["SEXO"] == "hombre").sum())
    m_atp = int((atp_df["SEXO"] == "mujer").sum())
    assert h_atp == 339, f"Fallo ATP Hombres: esperado 339, obtenido {h_atp}"
    assert m_atp == 190, f"Fallo ATP Mujeres: esperado 190, obtenido {m_atp}"
    assert (h_atp + m_atp) == 529, "Fallo Total ATP"

    h_no_atp = int((no_atp_df["SEXO"] == "hombre").sum())
    m_no_atp = int((no_atp_df["SEXO"] == "mujer").sum())
    assert h_no_atp == 1790, f"Fallo No ATP Hombres: esperado 1790, obtenido {h_no_atp}"
    assert m_no_atp == 1004, f"Fallo No ATP Mujeres: esperado 1004, obtenido {m_no_atp}"
    assert (h_no_atp + m_no_atp) == 2794, "Fallo Total No ATP"

    # 3. Medias de superficie en ATP
    sup_h = float(atp_df[atp_df["SEXO"] == "hombre"]["SUPERFICIE_NUM"].mean())
    sup_m = float(atp_df[atp_df["SEXO"] == "mujer"]["SUPERFICIE_NUM"].mean())
    assert round(sup_h, 2) == 32.56, f"Fallo media superficie ATP H: esperado 32.56, obtenido {round(sup_h, 2)}"
    assert round(sup_m, 2) == 24.24, f"Fallo media superficie ATP M: esperado 24.24, obtenido {round(sup_m, 2)}"

    # 4. Distribución territorial en Enkarterrialde (ATP)
    enk_h = int(((atp_df["COMARCA"] == "ENKARTERRIALDE") & (atp_df["SEXO"] == "hombre")).sum())
    enk_m = int(((atp_df["COMARCA"] == "ENKARTERRIALDE") & (atp_df["SEXO"] == "mujer")).sum())
    assert enk_h == 107, f"Fallo Enkarterrialde ATP Hombres: esperado 107, obtenido {enk_h}"
    assert enk_m == 78, f"Fallo Enkarterrialde ATP Mujeres: esperado 78, obtenido {enk_m}"

    # 5. Validación de los métodos de agregación
    kpis = processor.get_macro_kpis()
    assert kpis["total_comerciales"] == 3323
    assert kpis["total_atp"] == 529
    assert kpis["total_no_atp"] == 2794

    df_age_4 = processor.get_age_distribution("ALL", "4_tramos")
    assert len(df_age_4) == 4
    assert list(df_age_4.columns) == ["Tramo", "Hombres", "Mujeres", "Total", "% Feminización", "Razón (M por 100 H)"]

    df_age_3 = processor.get_age_distribution("ATP", "3_tramos")
    assert len(df_age_3) == 3

    df_surf_agro = processor.get_surface_strata("ALL", "agronomico")
    assert len(df_surf_agro) == 4

    df_surf_clas = processor.get_surface_strata("ALL", "clasico")
    assert len(df_surf_clas) == 4

    df_sub = processor.get_subsectors_summary("ATP")
    assert len(df_sub) > 0

    df_jur = processor.get_legal_status_summary("ATP")
    assert len(df_jur) > 0

    df_terr = processor.get_territorial_summary("ATP")
    assert len(df_terr) == 6
    assert df_terr.loc[df_terr["Comarca"] == "ENKARTERRIALDE", "Hombres"].values[0] == 107
    assert df_terr.loc[df_terr["Comarca"] == "ENKARTERRIALDE", "Mujeres"].values[0] == 78

    df_eco = processor.get_sustainability_summary("ALL")
    assert len(df_eco) > 0

    print("✓ Todos los datos de Hoja1 validados correctamente contra las reglas de negocio.")
