import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import glob

# Agregar directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import download_sample_data, load_data_from_directory
from ecg_analyzer import analyze_heart_rate
from ecg_visualizer import plot_ecg_grid

# Configuración de la página
st.set_page_config(
    page_title="Visualizador de ECG",
    page_icon="❤️",
    layout="wide"
)

# Título de la aplicación
st.title("Visualizador de ECG para Análisis de Arritmias")
st.markdown("""
Esta aplicación permite visualizar y analizar señales de ECG de 12 derivaciones de la base de datos
[ECG Arrhythmia Database](https://physionet.org/content/ecg-arrhythmia/1.0.0/) de PhysioNet.
""")

# Definir directorio de datos
DATA_DIR = "data"

# Sidebar para opciones
st.sidebar.header("Configuración")

# Verificar si ya hay datos en el directorio
local_data, local_metadata = load_data_from_directory(DATA_DIR)

if local_data:
    st.sidebar.success(f"✅ Datos encontrados: {len(local_data)} registros")
    
    # Guardar en session_state
    st.session_state["data"] = local_data
    st.session_state["metadata"] = local_metadata
else:
    st.sidebar.warning("⚠️ No se encontraron datos locales")

# Opciones para cargar datos
load_option = st.sidebar.radio(
    "Opciones de carga de datos:",
    ["Usar datos existentes", "Descargar muestra pequeña"]
)

# Botón para descargar datos
if load_option == "Descargar muestra pequeña":
    num_records = st.sidebar.slider("Número de registros a descargar", 1, 10, 3)
    
    if st.sidebar.button("Descargar muestra de datos"):
        with st.spinner("Descargando datos de PhysioNet..."):
            data, metadata = download_sample_data(num_records=num_records, data_dir=DATA_DIR)
            st.session_state["data"] = data
            st.session_state["metadata"] = metadata
            st.sidebar.success(f"✅ Datos descargados: {len(data)} registros")

# Mostrar datos disponibles si existen
if "data" in st.session_state and "metadata" in st.session_state:
    data = st.session_state["data"]
    metadata = st.session_state["metadata"]
    
    if not data:
        st.info("No hay datos disponibles. Por favor, descarga una muestra o carga datos locales.")
    else:
        # Seleccionar registro para visualizar
        record_ids = list(data.keys())
        selected_record = st.sidebar.selectbox("Seleccionar registro", record_ids)
        
        # Mostrar info del registro
        st.markdown(f"### Registro: {selected_record}")
        
        if "comments" in metadata[selected_record]:
            st.markdown(f"**Diagnóstico:** {metadata[selected_record]['comments']}")
        
        # Seleccionar derivación para análisis
        leads = list(data[selected_record]['signal_names'])
        selected_lead = st.sidebar.selectbox(
            "Seleccionar derivación para análisis",
            leads,
            index=leads.index('II') if 'II' in leads else 0  # Derivación II por defecto
        )
        
        # Obtener señal y frecuencia de muestreo
        signal = data[selected_record]['signals']
        signal_names = data[selected_record]['signal_names']
        fs = data[selected_record]['fs']
        
        # Análisis de frecuencia cardíaca
        lead_idx = signal_names.index(selected_lead)
        lead_signal = signal[:, lead_idx]
        
        peaks, heart_rate, rr_intervals = analyze_heart_rate(lead_signal, fs)
        
        # Mostrar frecuencia cardíaca
        st.markdown("### Análisis de Frecuencia Cardíaca")
        
        col1, col2 = st.columns(2)
        
        with col1:
            is_normal = 60 <= heart_rate <= 100
            
            # Usar st.markdown en lugar de st.metric para evitar el icono de flecha
            heart_rate_value = f"<h3>Frecuencia Cardíaca: {heart_rate:.1f} lpm</h3>"
            
            if is_normal:
                status = '<p style="color:#00cc96; font-size:18px; margin-top:-15px;">● Normal</p>'
            elif heart_rate > 100:
                status = '<p style="color:#ff4b4b; font-size:18px; margin-top:-15px;">↑ Taquicardia</p>'
            else:  # heart_rate < 60
                status = '<p style="color:#ff4b4b; font-size:18px; margin-top:-15px;">↓ Bradicardia</p>'
                
            st.markdown(heart_rate_value + status, unsafe_allow_html=True)
        
        with col2:
            if heart_rate < 60:
                st.warning("⚠️ Bradicardia detectada (FC < 60 lpm)")
            elif heart_rate > 100:
                st.warning("⚠️ Taquicardia detectada (FC > 100 lpm)")
            else:
                st.success("✅ Frecuencia cardíaca normal (60-100 lpm)")
            
            # Aplicar estilo CSS para colorear el fondo del mensaje de warning en el mismo rojo
            st.markdown("""
            <style>
            .stWarning {
                background-color: rgba(255, 75, 75, 0.2) !important;
                border-left-color: #ff4b4b !important;
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Visualización de ECG
        st.markdown("### Visualización de ECG")
        
        # Mostrar todas las derivaciones en una cuadrícula
        tab1, tab2 = st.tabs(["Vista 12 derivaciones", "Vista detallada"])
        
        with tab1:
            fig = plt.figure(figsize=(15, 10))
            for i, lead_name in enumerate(signal_names):
                lead_sig = signal[:, i]
                ax = fig.add_subplot(3, 4, i+1)
                plot_ecg_grid(ax, lead_sig, fs, lead_name)
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            # Mostrar derivación seleccionada con detalle
            fig, ax = plt.subplots(figsize=(15, 5))
            plot_ecg_grid(ax, lead_signal, fs, selected_lead, peaks=peaks)
            st.pyplot(fig)
            
            # Mostrar intervalo RR promedio
            st.markdown(f"**Intervalo RR promedio:** {np.mean(rr_intervals):.2f} segundos")
            
            # Histograma de intervalos RR
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.hist(rr_intervals, bins=20, alpha=0.7)
            ax.set_xlabel("Intervalo RR (s)")
            ax.set_ylabel("Frecuencia")
            ax.set_title("Distribución de Intervalos RR")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

else:
    st.info("👈 Selecciona una opción de carga de datos en el panel lateral para comenzar")
    