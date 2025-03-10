import random
import os

# Вхідні параметри
N_sequence = 100  # Розмір послідовності
N1 = 13  # Порядковий номер студента у журналі групи (замініть на свій)
N0 = N_sequence - N1  # Кількість нулів

# Створення списків
list1 = ['1'] * N1
list0 = ['0'] * N0

# Об'єднання та перемішування
sequence_list = list1 + list0
random.shuffle(sequence_list)

# Формування рядкової послідовності
original_sequence_1 = ''.join(sequence_list)

# Визначення розміру алфавіту
unique_chars = set(original_sequence_1)
sequence_alphabet_size = len(unique_chars)

# Обчислення кількості байтів для збереження
original_sequence_size_bytes = len(original_sequence_1)  # У байтах

# Створення директорії, якщо її немає
output_dir = "LosslessСompression"
os.makedirs(output_dir, exist_ok=True)

# Запис у файл results_sequence.txt
output_file = os.path.join(output_dir, "results_sequence.txt")
with open(output_file, "w", encoding="utf-8") as file:
    file.write(f"Послідовність: {original_sequence_1}\n")
    file.write(f"Розмір послідовності: {original_sequence_size_bytes} byte\n")
    file.write(f"Розмір алфавіту: {sequence_alphabet_size}\n")
    file.write("-" * 50 + "\n")

print("Тестова послідовність №1 успішно збережена у results_sequence.txt")
