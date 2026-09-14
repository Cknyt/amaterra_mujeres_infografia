# AMATERRA · Analítica de Datos Agrarios (Mujeres)

Plataforma analítica y cuadro de mando interactivo desarrollado en **Streamlit** para la visualización, exploración y generación automatizada de informes ejecutivos en **Microsoft PowerPoint (`.pptx`)**.

---

## 🛠️ Arquitectura del Proyecto

```plaintext
.
├── .gitignore
├── requirements.txt
├── README.md
├── AMATERRA_Mujeres_DatosExplotacionesAlta_Datos01.xlsx  (Fichero fuente existente en raíz)
├── src/
│   ├── __init__.py
│   ├── config.py           # Constantes, paletas de color y mapeos canónicos
│   ├── data_processor.py   # ETL, filtros y agregaciones desde Hoja1
│   ├── visualizer.py       # Gráficos Plotly interactivos (Sankey, barras, pirámides)
│   └── exporter.py         # Motor de generación de PPTX y exportación de tablas
├── exports/
│   ├── charts/             # Salida para .png (300 dpi) y .svg
│   └── tables/             # Salida para reportes .xlsx consolidados
├── app.py                  # Entrypoint de la aplicación Streamlit
└── verify_setup.py         # Script de verificación integral del entorno y módulos
```

---

## 🚀 Guía de Inicio Rápido

### 1. Requisitos Previos
- Python 3.10 o superior (compatible con Python 3.13).

### 2. Activación del Entorno Virtual (`.venv`)

#### En Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```
*Nota: Si PowerShell restringe la ejecución de scripts, ejecuta antes: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.*

#### En Windows (CMD):
```cmd
.venv\Scripts\activate.bat
```

#### En Linux / macOS:
```bash
source .venv/bin/activate
```

---

### 3. Instalación de Dependencias

Si necesitas reinstalar o actualizar las dependencias en el entorno activo:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Ejecución de la Aplicación

Para lanzar la aplicación interactiva de Streamlit:

**Con el entorno virtual activado:**
```bash
streamlit run app.py
```

**O directamente en Windows sin necesidad de activar previamente:**
```powershell
.venv\Scripts\python -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web en: `http://localhost:8501`.

---

## 📊 Funcionalidades Clave

1. **Panel Ejecutivo**:
   - Tarjetas de KPIs cuantitativos (total de explotaciones, superficies estimadas, porcentajes).
   - Gráficos interactivos generados con Plotly con paleta agraria personalizada.
2. **Explorador y Filtrado Dinámico**:
   - Filtros multiselección por variables categóricas.
   - Tabla interactiva con búsqueda, ordenación y descarga directa en formato CSV.
3. **Motor de Exportación a PowerPoint**:
   - Diapositivas de portada y branding institucional.
   - Tarjetas de KPIs convertidas en elementos visuales nativos de PowerPoint.
   - Conversión de gráficos Plotly en imágenes de alta resolución mediante **Kaleido**.
   - Tablas formateadas con estilos corporativos.
   - Descarga directa desde el navegador web y guardado en la carpeta `exports/`.
