
# Visualizador de ECG para Análisis de Arritmias

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplicación para visualizar y analizar señales de ECG de 12 derivaciones provenientes de la base de datos [ECG Arrhythmia Database](https://physionet.org/content/ecg-arrhythmia/1.0.0/) de PhysioNet.

![ECG Visualizer Demo](https://via.placeholder.com/800x400?text=ECG+Visualizer+Screenshot)

## Características

- Visualización de ECG siguiendo las reglas del papel electrocardiográfico
  - Cuadrícula de 0.1mV x 0.04s (cuadros pequeños)
  - Cuadrícula de 0.5mV x 0.2s (cuadros grandes)
- Análisis de frecuencia cardíaca
  - Detección automática de picos R usando neurokit2
  - Cálculo de frecuencia cardíaca
  - Alertas para frecuencias fuera del rango normal
  - Indicadores visuales para:
    - Normal (60-100 lpm): Círculo verde
    - Taquicardia (>100 lpm): Flecha roja hacia arriba
    - Bradicardia (<60 lpm): Flecha roja hacia abajo
- Visualización de 12 derivaciones estándar en formato de cuadrícula
- Vista detallada con histograma de intervalos RR
- Soporte para dataset completo o muestra pequeña de PhysioNet

## Demo

Puedes probar la aplicación en [Streamlit Cloud](https://share.streamlit.io/) (Actualiza este enlace cuando hayas desplegado la aplicación).

## Instalación

### Requisitos previos

- Python 3.9 o superior
- Git
- Conexión a Internet (para descargar datos de PhysioNet)

### Opción 1: Usando Conda

1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/visualizador-ecg.git
cd visualizador-ecg
```

2. Crea un entorno conda con las dependencias:
```bash
conda env create -f environment.yml
conda activate ecg_app
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

### Opción 2: Usando Pip

1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/visualizador-ecg.git
cd visualizador-ecg
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## Uso

### Con muestra pequeña de datos

1. Una vez iniciada la aplicación, selecciona "Descargar muestra pequeña" en el panel lateral.
2. Selecciona la cantidad de registros a descargar y haz clic en "Descargar muestra de datos".
3. Selecciona un registro ECG de la lista desplegable.
4. Explora las diferentes derivaciones y analiza la frecuencia cardíaca.

### Con dataset completo

1. Descarga el dataset completo de [PhysioNet](https://physionet.org/content/ecg-arrhythmia/1.0.0/).
2. Extrae el contenido en el directorio `data` del proyecto.
3. Inicia la aplicación y selecciona "Usar datos existentes".
4. La aplicación detectará automáticamente los registros disponibles.

## Estructura del Proyecto

```
visualizador-ecg/
├── app.py                  # Punto de entrada principal de la aplicación Streamlit
├── src/                    # Módulos de código fuente
│   ├── data_loader.py      # Funciones para carga y descarga de datos
│   ├── ecg_analyzer.py     # Funciones para análisis de ECG y frecuencia cardíaca
│   └── ecg_visualizer.py   # Funciones para visualización de ECG
├── data/                   # Directorio para archivos de datos
├── environment.yml         # Archivo de entorno conda
├── requirements.txt        # Dependencias para pip
└── README.md               # Este archivo
```

## Estructura del directorio de datos
```
data/
├── RECORDS                 # Lista de todos los registros
├── record1/                # Directorio para cada registro
│   ├── record1.dat         # Archivo de datos
│   └── record1.hea         # Archivo de cabecera
├── record2/
│   ├── record2.dat
│   └── record2.hea
└── ...
```

## Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/visualizador-ecg.git
git push -u origin main
```

2. Para desplegar en Streamlit Cloud:
   - Inicia sesión en [Streamlit Community Cloud](https://streamlit.io/cloud) con tu cuenta de GitHub
   - Haz clic en "New app"
   - Selecciona tu repositorio, rama (main) y archivo (app.py)
   - Haz clic en "Deploy"

### Configuración Adicional para Streamlit Cloud
- Si tu aplicación necesita descargar datos durante el despliegue, considera:
  - Añadir un pequeño conjunto de datos de ejemplo en el repositorio
  - Utilizar [secretos de Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) para APIs o credenciales
  - Configurar [dependencias específicas de Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/app-dependencies)

## Consideraciones Técnicas

- El dataset completo tiene aproximadamente 5GB, por lo que se recomienda:
  - Para desarrollo: usar la función de descarga de muestra pequeña
  - Para producción: preparar el directorio `data` con registros seleccionados
- Se utiliza la librería neurokit2 para el procesamiento y análisis de señales ECG
- La visualización sigue los estándares del papel electrocardiográfico:
  - Velocidad horizontal: 25 mm/s
  - Sensibilidad vertical: 10 mm/mV

## Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del proyecto
2. Crea una rama con tu función (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

## Christian Amao Suxo
## Dennis Sandoval Huamán
## Jose Piñas Rivera -  jpinas@pucp.pe

Enlace del proyecto: [https://github.com/TU_USUARIO/visualizador-ecg](https://github.com/TU_USUARIO/visualizador-ecg)

