import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft

# Параметри сигналу
a = 0  # Середнє значення
b = 10  # Стандартне відхилення
n = 500  # Кількість точок
Fs = 1000  # Частота дискретизації (Гц)
F_max = 29  # Максимальна частота сигналу (Гц)
F_filter = 36  # Полоса пропуску фільтру

# Генерація випадкового сигналу
signal_data = np.random.normal(a, b, n)

# Визначення часу
time_values = np.arange(n) / Fs

# Нормування частоти
w = F_max / (Fs / 2)

# Розрахунок параметрів ФНЧ
sos = signal.butter(3, w, 'low', output='sos')

# Двонаправлена фільтрація
filtered_signal = signal.sosfiltfilt(sos, signal_data)


# Функція для побудови графіків
def plot_signal(x, y, title, xlabel, ylabel, filename):
    save_dir = "./figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = f"{save_dir}/{filename}.png"
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1, color='tab:blue')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    fig.savefig(save_path, dpi=600)
    plt.show()


# Дискретизація сигналу
dt_values = [2, 4, 8, 16]
discrete_signals = []
discrete_spectrums = []
restored_signals = []
discrepancy_vars = []
snr_values = []

for Dt in dt_values:
    discrete_signal = np.zeros(n)
    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = filtered_signal[i * Dt]
    discrete_signals.append(discrete_signal)

    # Розрахунок спектру
    spectrum = fft.fft(discrete_signal)
    spectrum_shifted = np.abs(fft.fftshift(spectrum))
    discrete_spectrums.append(spectrum_shifted)

    # Відновлення сигналу
    w_filter = F_filter / (Fs / 2)
    sos_filter = signal.butter(3, w_filter, 'low', output='sos')
    restored_signal = signal.sosfiltfilt(sos_filter, discrete_signal)
    restored_signals.append(restored_signal)

    # Розрахунок похибок
    error = restored_signal - filtered_signal
    variance_error = np.var(error)
    discrepancy_vars.append(variance_error)
    snr = np.var(filtered_signal) / variance_error if variance_error != 0 else np.inf
    snr_values.append(snr)

# Побудова графіків дискретизованих сигналів
fig, axes = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
for i, ax in enumerate(axes.flat):
    ax.plot(time_values, discrete_signals[i], linewidth=1)
    ax.set_title(f'Dt = {dt_values[i]}', fontsize=12)
fig.savefig("./figures/discrete_signals.png", dpi=600)
plt.show()

# Побудова графіку дисперсії
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(dt_values, discrepancy_vars, marker='o', linestyle='-', color='r')
plt.xlabel("Крок дискретизації (Dt)", fontsize=14)
plt.ylabel("Дисперсія", fontsize=14)
plt.title("Залежність дисперсії від Dt", fontsize=14)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.savefig("./figures/discrepancy_variance.png", dpi=600)
plt.show()

# Побудова графіку SNR
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(dt_values, snr_values, marker='o', linestyle='-', color='g')
plt.xlabel("Крок дискретизації (Dt)", fontsize=14)
plt.ylabel("SNR", fontsize=14)
plt.title("Співвідношення сигнал-шум (SNR)", fontsize=14)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.savefig("./figures/snr.png", dpi=600)
plt.show()
