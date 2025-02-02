import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft

# Параметри сигналу
a = 0      # Середнє значення
b = 10     # Стандартне відхилення
n = 500   # Кількість точок
Fs = 1000  # Частота дискретизації (Гц)
F_max = 29  # Максимальна частота сигналу (Гц)

# Генерація випадкового сигналу
signal_data = np.random.normal(a, b, n)

# Визначення часу
time_values = np.arange(n) / Fs

# Нормування частоти
w = F_max / (Fs / 2)

# Розрахунок параметрів ФНЧ
sos = signal.butter(3, w, 'low', output='sos')

# Двонаправлена фільтрація для уникнення фазових зсувів
filtered_signal = signal.sosfiltfilt(sos, signal_data)

# Побудова графіка сигналу
def plot_signal(x, y, title, xlabel, ylabel, filename):
    # Створюємо папку, якщо вона не існує
    save_dir = "./figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = f"{save_dir}/{filename}.png"

    # Створення фігури та осей з необхідними розмірами
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))  # 21 см × 14 см

    # Побудова графіка
    ax.plot(x, y, linewidth=1, color='tab:blue')  # Колір і товщина лінії

    # Додавання підписів
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)

    # Додавання сітки у стилі зразка
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # Збереження графіка
    fig.savefig(save_path, dpi=600)

    # Відображення графіка
    plt.show()


# Побудова графіка сигналу
plot_signal(time_values, filtered_signal,
            "Сигнал з максимальною частотою F_max = 29 Гц",
            "Час (секунди)",
            "Амплітуда сигналу",
            "filtered_signal")


# РОЗРАХУНОК СПЕКТРУ СИГНАЛУ
spectrum = fft.fft(filtered_signal)  # Перетворення Фур'є
spectrum_shifted = np.abs(fft.fftshift(spectrum))  # Модульний спектр + зсув

# Розрахунок частотних відліків
freq_values = fft.fftshift(fft.fftfreq(n, 1 / Fs))

# Побудова графіка спектра
plot_signal(freq_values, spectrum_shifted,
            "Амплітудний спектр сигналу",
            "Частота (Гц)",
            "Амплітуда спектра",
            "signal_spectrum")
