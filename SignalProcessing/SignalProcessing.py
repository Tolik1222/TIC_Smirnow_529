import numpy as np
import matplotlib.pyplot as plt

# Параметри сигналу
a = 0      # Середнє значення
b = 10     # Стандартне відхилення
n = 1000   # Кількість точок
Fs = 1000  # Частота дискретизації (Гц)

# Генерація випадкового сигналу
signal = np.random.normal(a, b, n)

# Визначення часу
time = np.arange(n) / Fs  # Масив часу

# Побудова графіка
plt.figure(figsize=(10, 4))
plt.plot(time, signal, label="Випадковий сигнал")
plt.xlabel("Час (с)")
plt.ylabel("Амплітуда")
plt.title("Згенерований випадковий сигнал у часовій області")
plt.legend()
plt.grid()
plt.savefig("SignalProcessing/figures/random_signal_with_time.png")  # Збереження графіка
plt.show()
