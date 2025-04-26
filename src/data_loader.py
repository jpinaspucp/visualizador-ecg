import os
import numpy as np
import requests
import tempfile
import zipfile
import wfdb
import random
import glob

# URL base de la base de datos
BASE_URL = "https://physionet.org/content/ecg-arrhythmia/1.0.0/"

def download_sample_data(num_records=5, data_dir="data"):
    """
    Descarga una muestra pequeña de datos de ECG de PhysioNet
    
    Args:
        num_records: Número de registros a descargar
        data_dir: Directorio donde se guardarán los datos
        
    Returns:
        dict: Diccionario con datos de ECG
        dict: Diccionario con metadatos
    """
    # Crear directorio si no existe
    os.makedirs(data_dir, exist_ok=True)
    
    # Descargar y leer la lista de registros si no existe
    record_list_path = os.path.join(data_dir, "RECORDS")
    if not os.path.exists(record_list_path):
        records_url = BASE_URL + "RECORDS"
        response = requests.get(records_url)
        response.raise_for_status()
        
        with open(record_list_path, "wb") as f:
            f.write(response.content)
    
    # Leer la lista de registros
    with open(record_list_path, "r") as f:
        all_records = [line.strip() for line in f.readlines()]
    
    # Seleccionar una muestra aleatoria
    sample_records = random.sample(all_records, min(num_records, len(all_records)))
    
    data = {}
    metadata = {}
    
    # Descargar cada registro
    for record_id in sample_records:
        record_dir = os.path.join(data_dir, record_id)
        os.makedirs(record_dir, exist_ok=True)
        
        # Descargar archivos necesarios
        for ext in [".hea", ".dat"]:
            file_url = f"{BASE_URL}{record_id}{ext}"
            local_file = os.path.join(record_dir, f"{record_id}{ext}")
            
            if not os.path.exists(local_file):
                response = requests.get(file_url)
                response.raise_for_status()
                
                with open(local_file, "wb") as f:
                    f.write(response.content)
        
        # Leer el registro
        record = wfdb.rdrecord(os.path.join(record_dir, record_id))
        
        # Extraer información
        signal_data = record.p_signal
        fs = record.fs
        signal_names = record.sig_name
        
        # Guardar metadatos
        metadata[record_id] = {
            'fs': fs,
            'n_leads': len(signal_names),
            'length_seconds': len(signal_data) / fs,
            'comments': record.comments[0] if record.comments else "No comments"
        }
        
        # Guardar datos
        data[record_id] = {
            'signals': signal_data,
            'signal_names': signal_names,
            'fs': fs
        }
    
    return data, metadata

def load_data_from_directory(data_dir="data"):
    """
    Carga los datos ECG desde un directorio local
    
    Args:
        data_dir: Directorio donde se encuentran los datos
        
    Returns:
        dict: Diccionario con datos de ECG
        dict: Diccionario con metadatos
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        return {}, {}
    
    # Buscar archivos .hea (cabeceras) en el directorio
    header_files = glob.glob(os.path.join(data_dir, "**", "*.hea"), recursive=True)
    
    data = {}
    metadata = {}
    
    for header_file in header_files:
        record_path = os.path.splitext(header_file)[0]
        record_id = os.path.basename(record_path)
        
        try:
            # Intentar leer el registro
            record = wfdb.rdrecord(record_path)
            
            # Extraer información
            signal_data = record.p_signal
            fs = record.fs
            signal_names = record.sig_name
            
            # Guardar metadatos
            metadata[record_id] = {
                'fs': fs,
                'n_leads': len(signal_names),
                'length_seconds': len(signal_data) / fs,
                'comments': record.comments[0] if record.comments else "No comments",
                'file_path': record_path
            }
            
            # Guardar datos
            data[record_id] = {
                'signals': signal_data,
                'signal_names': signal_names,
                'fs': fs
            }
        except Exception as e:
            print(f"Error al cargar el registro {record_id}: {e}")
    
    return data, metadata

