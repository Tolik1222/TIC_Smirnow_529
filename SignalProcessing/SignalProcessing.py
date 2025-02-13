import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

# Створення директорії для збереження графіків
os.makedirs("figures", exist_ok=True)

# Параметри сигналу
a, b, n, Fs, F_max = 0, 10, 500, 1000, 29

# Генерація випадкового сигналу
signal_data = np.random.normal(a, b, n)

# Визначення часу
time_values = np.arange(n) / Fs

# Нормування частоти та розрахунок параметрів ФНЧ
sos = signal.butter(3, F_max / (Fs / 2), 'low', output='sos')
filtered_signal = signal.sosfiltfilt(sos, signal_data)

# Рівні квантування
quant_levels = [4, 16, 64, 256]
quantized_signals, quantization_errors, snr_values, variances = [], [], [], []

# Дисперсія початкового сигналу
initial_variance = np.var(filtered_signal)
print(f"Дисперсія початкового сигналу: {initial_variance}")

# Квантування та аналіз сигналу
for M in quant_levels:
    delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)
    quantized_signal = delta * np.round(filtered_signal / delta)
    quantized_signals.append(quantized_signal)

    quant_error = filtered_signal - quantized_signal
    quantization_errors.append(np.var(quant_error))

    snr_values.append(np.var(filtered_signal) / np.var(quant_error) if np.var(quant_error) != 0 else np.inf)
    variances.append(np.var(quantized_signal))

# Побудова графіків
fig, ax = plt.subplots(figsize=(10, 5))
for i, M in enumerate(quant_levels):
    ax.plot(time_values, quantized_signals[i], label=f'M = {M}', linewidth=0.8)
ax.legend()
ax.set_xlabel("Час (с)")
ax.set_ylabel("Амплітуда")
ax.set_title("Квантування сигналу")
ax.grid(True)
plt.savefig("figures/quantization.png", dpi=300, bbox_inches='tight')
plt.show()

fig, axs = plt.subplots(2, 2, figsize=(10, 6))
fig.suptitle("Цифрові сигнали з рівнями квантування")
for i, ax in enumerate(axs.flatten()):
    ax.plot(time_values, quantized_signals[i], linewidth=0.8)
    ax.set_title(f"M = {quant_levels[i]}")
    ax.set_xlabel("Час (с)")
    ax.set_ylabel("Амплітуда")
    ax.grid(True)
plt.tight_layout()
plt.savefig("figures/digital_signals.png", dpi=300, bbox_inches='tight')
plt.show()

# Графік SNR
plt.figure(figsize=(8, 5))
plt.plot(quant_levels, snr_values, marker='o', linestyle='-', color='g')
plt.xlabel("Кількість рівнів квантування")
plt.ylabel("SNR")
plt.title("Співвідношення сигнал-шум (SNR)")
plt.grid(True)
plt.savefig("figures/snr_vs_quantization_levels.png", dpi=300, bbox_inches='tight')
plt.show()

# Графік дисперсії
plt.figure(figsize=(8, 5))
plt.plot(quant_levels, variances, marker='o', linestyle='-', color='b')
plt.xlabel("Кількість рівнів квантування")
plt.ylabel("Дисперсія")
plt.title("Залежність дисперсії від рівнів квантування")
plt.grid(True)
plt.xscale('log')
plt.savefig("figures/variance_vs_quantization_levels.png", dpi=300, bbox_inches='tight')
plt.show()

# Таблиця значень та кодів
M = 16
quantize_levels = np.linspace(np.min(filtered_signal), np.max(filtered_signal), M)
table_data = pd.DataFrame({
    "Значення сигналу": quantize_levels,
    "Кодова послідовність": [format(i, f'0{int(np.log2(M))}b') for i in range(M)]
})

fig, ax = plt.subplots(figsize=(6, 4))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center')
plt.savefig("figures/quantization_table.png", dpi=300, bbox_inches='tight')
plt.show()

# Графік бітової послідовності
bits = ''.join([format(
    int(np.round((value - np.min(filtered_signal)) / delta)) if value >= np.min(filtered_signal) else 0,
    f'0{int(np.log2(M))}b') for value in quantized_signals[1]])
bit_sequence = [int(bit) for bit in bits if bit in '01']

fig, ax = plt.subplots(figsize=(10, 5))
ax.step(range(len(bit_sequence)), bit_sequence, linewidth=0.1)
ax.set_xlabel("Час (відлік)")
ax.set_ylabel("Бітова послідовність")
ax.set_title(f"Графік бітової послідовності для M={M}")
ax.grid(True)
plt.savefig("figures/bit_sequence.png", dpi=300, bbox_inches='tight')
plt.show()
