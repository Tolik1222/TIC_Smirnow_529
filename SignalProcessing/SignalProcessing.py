import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметри сигналу
a = 0      # Середнє значення
b = 10     # Стандартне відхилення
n = 1000   # Кількість точок
Fs = 1000  # Частота дискретизації (Гц)
F_max = 100  # Максимальна частота сигналу (Гц)

# Генерація випадкового сигналу
signal_data = np.random.normal(a, b, n)

# Визначення часу
time = np.arange(n) / Fs

# Нормування частоти
w = F_max / (Fs / 2)

# Розрахунок параметрів ФНЧ
sos = signal.butter(3, w, 'low', output='sos')

# Двонаправлена фільтрація для уникнення фазових зсувів
filtered_signal = signal.sosfiltfilt(sos, signal_data)

# Переконуємося, що директорія для збереження графіків існує
figures_dir = "SignalProcessing/figures"
os.makedirs(figures_dir, exist_ok=True)

# Побудова графіка
plt.figure(figsize=(10, 4))
plt.plot(time, signal_data, label="Оригінальний сигнал", alpha=0.5)
plt.plot(time, filtered_signal, label="Фільтрований сигнал (ФНЧ, sosfiltfilt)", linewidth=2)
plt.xlabel("Час (с)")
plt.ylabel("Амплітуда")
plt.title("Застосування фільтра низьких частот (sosfiltfilt)")
plt.legend()
plt.grid()
plt.savefig(os.path.join(figures_dir, "filtered_signal_filtfilt.png"))  # Збереження графіка
plt.show()
