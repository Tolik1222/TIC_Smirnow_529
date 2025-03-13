import random
import os
import string
import collections
import math
import matplotlib.pyplot as plt


def generate_sequence_1(n1, total_length=100):
    list1 = ['1'] * n1
    list0 = ['0'] * (total_length - n1)
    sequence = list1 + list0
    random.shuffle(sequence)
    return ''.join(sequence)


def generate_sequence_2(surname, total_length=100):
    list1 = list(surname)
    list0 = ['0'] * (total_length - len(surname))
    sequence = list1 + list0
    return ''.join(sequence)


def generate_sequence_3(surname, total_length=100):
    list1 = list(surname)
    list0 = ['0'] * (total_length - len(surname))
    sequence = list1 + list0
    random.shuffle(sequence)
    return ''.join(sequence)


def generate_sequence_4(surname, group_number, total_length=100):
    letters = list(surname) + list(group_number)
    n_letters = len(letters)
    n_repeats = total_length // n_letters
    remainder = total_length % n_letters
    sequence = (letters * n_repeats) + letters[:remainder]
    return ''.join(sequence)


def generate_sequence_5(surname, group_number, total_length=100):
    elements = list(surname[:2]) + list(group_number)
    sequence = elements * (total_length // len(elements))
    random.shuffle(sequence)
    return ''.join(sequence)



def generate_sequence_6(surname, group_number, total_length=100):
    letters = list(surname[:2])
    digits = list(group_number)
    n_letters = int(0.7 * total_length)
    n_digits = total_length - n_letters
    sequence = [random.choice(letters) for _ in range(n_letters)] + [random.choice(digits) for _ in range(n_digits)]
    random.shuffle(sequence)
    return ''.join(sequence)


def generate_sequence_7(total_length=100):
    elements = string.ascii_lowercase + string.digits
    sequence = [random.choice(elements) for _ in range(total_length)]
    return ''.join(sequence)


def generate_sequence_8(total_length=100):
    return '1' * total_length


def calculate_probabilities(sequence):
    counts = collections.Counter(sequence)
    total_length = len(sequence)
    return {symbol: count / total_length for symbol, count in counts.items()}


def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values() if p > 0)


def calculate_source_excess(entropy, alphabet_size):
    return 1 - entropy / math.log2(alphabet_size) if alphabet_size > 1 else 1


def determine_uniformity(probabilities):
    mean_probability = sum(probabilities.values()) / len(probabilities)
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probabilities.values())
    return "рівна" if equal else "нерівна", mean_probability


student_number = 13
test_surname = "Смірнов"
group_number = "529"

original_sequences = [
    generate_sequence_1(student_number),
    generate_sequence_2(test_surname),
    generate_sequence_3(test_surname),
    generate_sequence_4(test_surname, group_number),
    generate_sequence_5(test_surname, group_number),
    generate_sequence_6(test_surname, group_number),
    generate_sequence_7(),
    generate_sequence_8()
]

os.makedirs("LosslessСompression", exist_ok=True)

results = []

with open("LosslessСompression/results_sequence.txt", "w", encoding="utf-8") as file:
    for i, seq in enumerate(original_sequences, start=1):
        alphabet_size = len(set(seq))
        size_bytes = len(seq)
        probabilities = calculate_probabilities(seq)
        entropy = calculate_entropy(probabilities)
        source_excess = calculate_source_excess(entropy, alphabet_size)
        uniformity, mean_probability = determine_uniformity(probabilities)
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probabilities.items()])

        file.write(f"Послідовність {i}: {seq}\n")
        file.write(f"Розмір послідовності: {size_bytes} byte\n")
        file.write(f"Розмір алфавіту: {alphabet_size}\n")
        file.write(f"Ймовірності: {probability_str}\n")
        file.write(f"Середнє арифметичне ймовірностей: {mean_probability:.4f}\n")
        file.write(f"Тип розподілу: {uniformity}\n")
        file.write(f"Ентропія: {entropy:.4f}\n")
        file.write(f"Надмірність джерела: {source_excess:.4f}\n\n")

        results.append([alphabet_size, round(entropy, 2), round(source_excess, 2), uniformity])

# Створюємо папку, якщо вона ще не існує
os.makedirs("LosslessСompression", exist_ok=True)

# Записуємо результати аналізу у файл results_sequence.txt
with open("LosslessСompression/results_sequence.txt", "w", encoding="utf-8") as file:
    for i, seq in enumerate(original_sequences, start=1):
        alphabet_size = len(set(seq))
        size_bytes = len(seq)
        probabilities = calculate_probabilities(seq)
        entropy = calculate_entropy(probabilities)
        source_excess = calculate_source_excess(entropy, alphabet_size)
        uniformity, mean_probability = determine_uniformity(probabilities)
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probabilities.items()])

        file.write(f"Послідовність {i}: {seq}\n")
        file.write(f"Розмір послідовності: {size_bytes} byte\n")
        file.write(f"Розмір алфавіту: {alphabet_size}\n")
        file.write(f"Ймовірності: {probability_str}\n")
        file.write(f"Середнє арифметичне ймовірностей: {mean_probability:.4f}\n")
        file.write(f"Тип розподілу: {uniformity}\n")
        file.write(f"Ентропія: {entropy:.4f}\n")
        file.write(f"Надмірність джерела: {source_excess:.4f}\n\n")

# Записуємо створені послідовності у файл sequence.txt одним рядком, через кому
with open("LosslessСompression/sequence.txt", "w", encoding="utf-8") as seq_file:
    seq_file.write(",".join(original_sequences))



fig, ax = plt.subplots(figsize=(14 / 1.54, len(original_sequences) / 1.54))
headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
rows = [f'Послідовність {i + 1}' for i in range(len(original_sequences))]

ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)

fig.savefig("LosslessСompression/Характеристики_сформованих_послідовностей.png")