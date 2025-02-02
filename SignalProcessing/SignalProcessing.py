import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметри сигналу
a = 0      # Середнє значення
b = 10     # Стандартне відхилення
n = 1000   # Кількість точок
Fs = 1000  # Частота дискретизації (Гц)
F_max = 15  # Максимальна частота сигналу (Гц)

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

# Переконуємося, що директорія для збереження графіків існує
figures_dir = "SignalProcessing/figures"
os.makedirs(figures_dir, exist_ok=True)

# Побудова графіка з оригінальним і фільтрованим сигналами
plt.figure(figsize=(10, 4))
plt.plot(time_values, signal_data, label="Оригінальний сигнал", alpha=0.5)
plt.plot(time_values, filtered_signal, label="Фільтрований сигнал (ФНЧ, sosfiltfilt)", linewidth=2)
plt.xlabel("Час (с)")
plt.ylabel("Амплітуда")
plt.title("Застосування фільтра низьких частот (sosfiltfilt)")
plt.legend()
plt.grid()
plt.savefig(os.path.join(figures_dir, "filtered_signal_filtfilt.png"))  # Збереження графіка
plt.show()


# Функція для побудови графіка в потрібному форматі
def plot_signal(x, y, title, xlabel, ylabel):
    # Створюємо папку, якщо вона не існує
    save_dir = "./figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = f"{save_dir}/{title}.png"

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


# Побудова графіка тільки для фільтрованого сигналу
plot_signal(time_values, filtered_signal,
            "Сигнал з максимальною частотою F_max = 15 Гц",
            "Час (секунди)",
            "Амплітуда сигналу")
