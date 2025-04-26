import numpy as np
import neurokit2 as nk

def analyze_heart_rate(signal, sampling_rate):
    """
    Analiza la frecuencia cardíaca utilizando neurokit2
    
    Args:
        signal: Señal ECG de una derivación
        sampling_rate: Frecuencia de muestreo en Hz
        
    Returns:
        peaks: Índices de los picos R detectados
        heart_rate: Frecuencia cardíaca calculada
        rr_intervals: Intervalos RR en segundos
    """
    # Limpiar la señal
    signal_cleaned = nk.ecg_clean(signal, sampling_rate=sampling_rate)
    
    # Detectar los picos R
    peaks, info = nk.ecg_peaks(signal_cleaned, sampling_rate=sampling_rate)
    
    # Obtener índices de los picos R
    r_peaks = np.where(peaks["ECG_R_Peaks"] == 1)[0]
    
    # Calcular intervalos RR en segundos
    rr_intervals = np.diff(r_peaks) / sampling_rate
    
    # Calcular frecuencia cardíaca como 60 / promedio de intervalos RR
    if len(rr_intervals) > 0:
        heart_rate = 60 / np.mean(rr_intervals)
    else:
        heart_rate = 0
    
    return r_peaks, heart_rate, rr_intervals
