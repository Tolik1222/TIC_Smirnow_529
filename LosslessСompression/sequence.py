import random

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


student_number = 13  #
test_surname = "Смірнов"

original_sequence_1 = generate_sequence_1(student_number)
original_sequence_2 = generate_sequence_2(test_surname)
original_sequence_3 = generate_sequence_3(test_surname)

original_sequences = [original_sequence_1, original_sequence_2, original_sequence_3]

with open("LosslessСompression/results_sequence.txt", "a", encoding="utf-8") as file:
    for i, seq in enumerate(original_sequences, start=1):
        alphabet_size = len(set(seq))
        size_bytes = len(seq)
        file.write(f"Послідовність {i}: {seq}\n")
        file.write(f"Розмір послідовності {size_bytes} byte\n")
        file.write(f"Розмір алфавіту: {alphabet_size}\n\n")