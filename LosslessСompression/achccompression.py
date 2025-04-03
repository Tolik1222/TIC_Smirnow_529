import math
import collections
import matplotlib.pyplot as plt

def encode_ac(unique_chars, probabilitys, alphabet_size, sequence):
    alphabet = list(unique_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range += probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])

    # Перевірка нормалізації ймовірностей
    total_prob = sum(probability)
    if not (0.999 <= total_prob <= 1.001):  # Жорсткіша перевірка
        raise ValueError(f"Ймовірності не нормалізовані: sum={total_prob}")

    # Якщо всі символи однакові, повертаємо тривіальний результат
    if len(set(sequence)) == 1:
        point = 0.5  # Будь-яка точка в [0, 1)
        binary_code = "0" * len(sequence)  # Просте кодування
        return [point, alphabet_size, alphabet, probability], binary_code

    for i in range(len(sequence) - 1):
        for j in range(len(unity)):
            if sequence[i] == unity[j][0]:
                probability_low = unity[j][1]
                probability_high = unity[j][2]
                diff = probability_high - probability_low
                for k in range(len(unity)):
                    unity[k][1] = probability_low
                    unity[k][2] = probability[k] * diff + probability_low
                    probability_low = unity[k][2]
                break

    low = 0
    high = 0
    for i in range(len(unity)):
        if unity[i][0] == sequence[-1]:
            low = unity[i][1]
            high = unity[i][2]
            break

    if high <= low:
        raise ValueError(f"Помилка: high ({high}) <= low ({low}) для символу {sequence[-1]}")

    point = (low + high) / 2
    cod = math.ceil(math.log2(1 / (high - low))) + 1
    binary_code = ""
    for _ in range(cod):
        point *= 2
        if point >= 1:
            binary_code += "1"
            point -= 1
        else:
            binary_code += "0"

    return [point, alphabet_size, alphabet, probability], binary_code

def decode_ac(encoded_data_ac, sequence_length):
    point, alphabet_size, alphabet, probability = encoded_data_ac
    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range += probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])

    # Якщо алфавіт має один символ, повертаємо повторення цього символу
    if alphabet_size == 1:
        return alphabet[0] * sequence_length

    decoded_sequence = ""
    current_point = point
    for _ in range(sequence_length):
        for j in range(len(unity)):
            # Використовуємо ширший діапазон для стабільності
            if unity[j][1] <= current_point <= unity[j][2]:
                prob_low = unity[j][1]
                prob_high = unity[j][2]
                diff = prob_high - prob_low
                decoded_sequence += unity[j][0]
                if diff > 0:  # Уникаємо ділення на 0
                    current_point = (current_point - prob_low) / diff
                # Оновлюємо інтервали
                for k in range(len(unity)):
                    unity[k][1] = prob_low
                    unity[k][2] = probability[k] * diff + prob_low
                break
        else:
            # Якщо символ не знайдено, додаємо перший символ як запасний варіант
            decoded_sequence += alphabet[0]
            break

    return decoded_sequence

def encode_ch(unique_chars, probabilitys, sequence):
    alphabet = list(unique_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    final = [[alphabet[i], probability[i]] for i in range(len(alphabet))]

    if len(set(probability)) == 1 and 1 in probability:
        symbol_code = [[alphabet[i], "1" * i + "0"] for i in range(len(alphabet))]
        encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
        return [encode, symbol_code], encode

    final.sort(key=lambda x: x[1])
    tree = []
    for _ in range(len(final) - 1):
        left = final.pop(0)
        right = final.pop(0)
        tot = left[1] + right[1]
        tree.append([left[0], right[0]])
        final.append([left[0] + right[0], tot])
        final.sort(key=lambda x: x[1])

    tree.reverse()
    symbol_code = []
    alphabet.sort()
    for i in range(len(alphabet)):
        code = ""
        for j in range(len(tree)):
            if alphabet[i] in tree[j][0]:
                code += "0"
                if alphabet[i] == tree[j][0]:
                    break
            elif alphabet[i] in tree[j][1]:
                code += "1"
                if alphabet[i] == tree[j][1]:
                    break
        symbol_code.append([alphabet[i], code])

    encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
    return [encode, symbol_code], encode

def decode_ch(encoded_sequence):
    encode, symbol_code = encoded_sequence
    sequence = ""
    current_code = ""

    for bit in encode:
        current_code += bit
        for sym, code in symbol_code:
            if current_code == code:
                sequence += sym
                current_code = ""
                break

    return sequence

# Читання послідовностей із файлу
with open("sequence.txt", "r", encoding="utf-8") as file:
    sequences = file.read().strip().split(",")

if len(sequences) != 8:
    raise ValueError(f"Помилка: Очікується 8 послідовностей, отримано {len(sequences)}")

for i, seq in enumerate(sequences, 1):
    if len(seq) != 100:
        raise ValueError(f"Помилка: Послідовність {i} має довжину {len(seq)} замість 100")

original_sequences = [seq[:10] for seq in sequences]

results = []
with open("results_AC_CH.txt", "w", encoding="utf-8") as f:
    for idx, sequence in enumerate(original_sequences, 1):
        sequence_length = len(sequence)
        unique_chars = set(sequence)
        sequence_alphabet_size = len(unique_chars)
        counts = collections.Counter(sequence)
        probability = {symbol: count / sequence_length for symbol, count in counts.items()}

        # Перевірка й обчислення ентропії
        if sequence_alphabet_size == 1:
            entropy = 0
        else:
            entropy = -sum(p * math.log2(p) for p in probability.values())
            if abs(entropy) < 1e-10:
                entropy = 0

        try:
            encoded_data_ac, encoded_sequence_ac = encode_ac(unique_chars, probability, sequence_alphabet_size, sequence)
            bps_ac = len(encoded_sequence_ac) / sequence_length
            decoded_ac = decode_ac(encoded_data_ac, sequence_length)
        except ValueError as e:
            print(f"Помилка в AC для послідовності {idx}: {e}")
            continue

        encoded_data_ch, encoded_sequence_ch = encode_ch(unique_chars, probability, sequence)
        bps_ch = len(encoded_sequence_ch) / sequence_length
        decoded_ch = decode_ch(encoded_data_ch)

        f.write(f"Оригінальна послідовність {idx}: {sequence}\n")
        f.write(f"Ентропія: {entropy:.4f}\n")
        f.write("Арифметичне кодування\n")
        f.write(f"Дані закодованої AC послідовності: {encoded_data_ac}\n")
        f.write(f"Закодована AC послідовність: {encoded_sequence_ac}\n")
        f.write(f"Значення bps при кодуванні AC: {bps_ac:.2f}\n")
        f.write(f"Декодована AC послідовність: {decoded_ac}\n")
        f.write("Кодування Хаффмана\n")
        f.write("| Алфавіт | Код символу |\n")
        f.write("|---------|-------------|\n")
        for sym, code in encoded_data_ch[1]:
            f.write(f"| {sym} | {code} |\n")
        f.write(f"Дані закодованої CH послідовності: {encoded_data_ch}\n")
        f.write(f"Закодована CH послідовність: {encoded_sequence_ch}\n")
        f.write(f"Значення bps при кодуванні CH: {bps_ch:.2f}\n")
        f.write(f"Декодована CH послідовність: {decoded_ch}\n\n")

        results.append([round(entropy, 2), round(bps_ac, 2), round(bps_ch, 2)])

N = len(original_sequences)
fig, ax = plt.subplots(figsize=(14 / 1.54, N / 1.54))
ax.axis('off')
headers = ['Ентропія', 'bps AC', 'bps CH']
rows = [f'Послідовність {i}' for i in range(1, N + 1)]
table = ax.table(cellText=results, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig("Результати стиснення методами АС та СН.png")
plt.close()

print("Практична робота виконана. Результати збережено в 'results_AC_CH.txt' та 'Результати стиснення методами АС та СН.png'.")