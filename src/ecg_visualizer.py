import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def plot_ecg_grid(ax, signal, fs, title="ECG", peaks=None, duration_sec=10):
    """
    Visualiza la señal ECG siguiendo las reglas del papel electrocardiográfico
    
    Args:
        ax: Eje de matplotlib
        signal: Señal ECG
        fs: Frecuencia de muestreo en Hz
        title: Título del gráfico
        peaks: Índices de los picos R (opcional)
        duration_sec: Duración en segundos a mostrar
    """
    # Configurar límites para mostrar solo los primeros duration_sec segundos
    n_samples = min(int(duration_sec * fs), len(signal))
    t = np.arange(n_samples) / fs  # Tiempo en segundos
    
    # Configurar grilla mayor (0.5mV x 0.2s)
    ax.grid(which='major', linestyle='-', linewidth=0.5, color='red', alpha=0.7)
    
    # Configurar grilla menor (0.1mV x 0.04s)
    ax.grid(which='minor', linestyle='-', linewidth=0.2, color='pink', alpha=0.4)
    ax.minorticks_on()
    
    # Configurar espaciado de la grilla
    # Horizontal: 25 mm/s -> 1 cuadro grande = 0.2s, 1 cuadro pequeño = 0.04s
    major_ticks_x = np.arange(0, duration_sec + 0.2, 0.2)
    minor_ticks_x = np.arange(0, duration_sec + 0.04, 0.04)
    
    # Vertical: 10 mm/mV -> 1 cuadro grande = 0.5mV, 1 cuadro pequeño = 0.1mV
    amplitude_range = max(abs(np.max(signal[:n_samples])), abs(np.min(signal[:n_samples]))) * 1.5
    major_ticks_y = np.arange(-amplitude_range, amplitude_range + 0.5, 0.5)
    minor_ticks_y = np.arange(-amplitude_range, amplitude_range + 0.1, 0.1)
    
    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)
    ax.set_yticks(major_ticks_y)
    ax.set_yticks(minor_ticks_y, minor=True)
    
    # Graficar señal
    ax.plot(t, signal[:n_samples], 'k-', linewidth=1.2)
    
    # Marcar picos R si se proporcionan
    if peaks is not None:
        valid_peaks = peaks[peaks < n_samples]
        ax.plot(valid_peaks / fs, signal[valid_peaks], 'ro', markersize=5)
    
    # Configurar etiquetas
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud (mV)')
    ax.set_title(title)
    
    # Ajustar límites
    ax.set_xlim([0, duration_sec])
    ax.set_ylim([-amplitude_range, amplitude_range])
    
    return ax
