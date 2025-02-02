import numpy
import matplotlib.pyplot as plt

# Параметри сигналу
a = 0  # Середнє значення
b = 10  # Стандартне відхилення
n = 1000  # Кількість точок

# Генерація випадкового сигналу
signal = numpy.random.normal(a, b, n)


# Побудова графіка
plt.figure(figsize=(10, 4))
plt.plot(signal, label="Випадковий сигнал")
plt.xlabel("Індекс")
plt.ylabel("Амплітуда")
plt.title("Згенерований випадковий сигнал")
plt.legend()
plt.grid()
plt.savefig("SignalProcessing/figures/random_signal.png")  # Збереження графіка
plt.show()
