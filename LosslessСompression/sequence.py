import random
import os
import string
import collections
import math

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
    sequence = [random.choice(elements) for _ in range(total_length)]
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

student_number = 13
test_surname = "Смірнов"
group_number = "529"

original_sequence_1 = generate_sequence_1(student_number)
original_sequence_2 = generate_sequence_2(test_surname)
original_sequence_3 = generate_sequence_3(test_surname)
original_sequence_4 = generate_sequence_4(test_surname, group_number)
original_sequence_5 = generate_sequence_5(test_surname, group_number)
original_sequence_6 = generate_sequence_6(test_surname, group_number)
original_sequence_7 = generate_sequence_7()
original_sequence_8 = generate_sequence_8()

original_sequences = [original_sequence_1, original_sequence_2, original_sequence_3, original_sequence_4, original_sequence_5, original_sequence_6, original_sequence_7, original_sequence_8]

os.makedirs("LosslessСompression", exist_ok=True)

with open("LosslessСompression/results_sequence.txt", "w", encoding="utf-8") as file:
    for i, seq in enumerate(original_sequences, start=1):
        alphabet_size = len(set(seq))
        size_bytes = len(seq)
        probabilities = calculate_probabilities(seq)
        entropy = calculate_entropy(probabilities)
        file.write(f"Послідовність {i}: {seq}\n")
        file.write(f"Розмір послідовності {size_bytes} byte\n")
        file.write(f"Розмір алфавіту: {alphabet_size}\n")
        file.write(f"Ентропія: {entropy:.4f}\n\n")