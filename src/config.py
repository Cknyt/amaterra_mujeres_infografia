"""Módulo de configuración central del proyecto.

Contiene rutas globales, mapeos canónicos comarcales, cortes numéricos
para tramos de edad y superficie, y paletas cromáticas estándar y accesibles.
"""

from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta relativa por defecto al fichero fuente Excel en raíz
DEFAULT_EXCEL_PATH = BASE_DIR / "AMATERRA_Mujeres_DatosExplotacionesAlta_Datos01.xlsx"

# Rutas de exportación
EXPORTS_DIR = BASE_DIR / "exports"
CHARTS_DIR = EXPORTS_DIR / "charts"
TABLES_DIR = EXPORTS_DIR / "tables"

# Asegurar existencia de carpetas de exportación
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Mapeo canónico de Oficinas Comarcales Agrarias (OCA) a Comarcas (ADR)
OCA_TO_COMARCA = {
    "BALMASEDA": "ENKARTERRIALDE",
    "KARRANTZA": "ENKARTERRIALDE",
    "MUNGIA": "JATAONDO",
    "IGORRE": "GORBEIALDE",
    "DURANGO": "URKIOLA",
    "GERNIKA": "URREMENDI",
    "MARKINA": "LEA ARTIBAI",
}

# Cortes numéricos para tramos de edad
# Formato 4 tramos: (min_inclusive, max_inclusive, etiqueta)
AGE_BRACKETS_4 = [
    (-float("inf"), 40, "Jóvenes (<41)"),
    (41, 54, "Adultos (41-54)"),
    (55, 64, "Madurez (55-64)"),
    (65, float("inf"), "Jubilación (>=65)"),
]

# Formato 3 tramos: (min_inclusive, max_inclusive, etiqueta)
AGE_BRACKETS_3 = [
    (-float("inf"), 40, "18-40 años"),
    (41, 55, "41-55 años"),
    (56, float("inf"), "Mayor de 55 años"),
]

# Cortes numéricos de superficie en hectáreas (ha)
SURFACE_BRACKETS = [
    (-float("inf"), 5, "Muy pequeña (<= 5 ha)"),
    (5.0001, 20, "Pequeña (5-20 ha)"),
    (20.0001, 50, "Mediana (20-50 ha)"),
    (50.0001, float("inf"), "Grande (> 50 ha)"),
]
SURFACE_BRACKETS_AGRONOMICO = SURFACE_BRACKETS

SURFACE_BRACKETS_CLASICO = [
    (-float("inf"), 1.9999, "< 2 ha"),
    (2.0, 5.0, "2 - 5 ha"),
    (5.0001, 10.0, "5 - 10 ha"),
    (10.0001, float("inf"), "> 10 ha"),
]

# Paletas cromáticas para distinción de género
# Paleta Estándar: Morado / Teal para Mujeres; Azul / Gris pizarra para Hombres
GENDER_PALETTE = {
    "Mujer": "#8E44AD",       # Púrpura / Amatista
    "Hombre": "#2980B9",      # Azul corporativo
    "Persona Física": "#16A085", # Teal / Verde azulado
    "Persona Jurídica": "#7F8C8D", # Gris pizarra
    "Indeterminado": "#BDC3C7",   # Gris claro
}

# Paleta Accesible (Colorblind safe / Okabe-Ito inspirada)
ACCESSIBLE_GENDER_PALETTE = {
    "Mujer": "#CC79A7",       # Magenta / Púrpura rojizo accesible
    "Hombre": "#0072B2",      # Azul accesible
    "Persona Física": "#009E73", # Verde azulado accesible
    "Persona Jurídica": "#E69F00", # Naranja dorado
    "Indeterminado": "#999999",   # Gris neutral
}

# Paleta agraria institucional AMATERRA
BRAND_PALETTE = {
    "primary": "#2D6A4F",
    "secondary": "#52B788",
    "accent": "#D88C51",
    "dark": "#1B4332",
    "light": "#F8F9FA",
    "muted": "#6C757D",
}

# Secuencia general para gráficos multivariables
PLOTLY_THEME_COLORS = [
    "#8E44AD",  # Morado (Mujer)
    "#2980B9",  # Azul (Hombre)
    "#2D6A4F",  # Verde bosque
    "#D88C51",  # Terracota
    "#16A085",  # Teal
    "#E67E22",  # Naranja
    "#34495E",  # Gris oscuro
]
