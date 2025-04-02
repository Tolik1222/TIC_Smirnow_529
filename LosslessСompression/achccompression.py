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

    for i in range(len(sequence) - 1):
        for j in range(len(unity)):
            if sequence[i] == unity[j][0]:
                probability_low = unity[j][1]
                probability_high = unity[j][2]
                diff = probability_high - probability_low
                for k in range(len(unity)):
                    unity[k][1] = probability_low
                    unity[k][2] = probability[k] * diff + probability_low
                break

    point = (unity[0][1] + unity[0][2]) / 2
    size_cod = int(-math.log2(min(probability))) + 1
    binary_code = ""
    for _ in range(size_cod):
        point *= 2
        if point > 1:
            binary_code += "1"
            point -= 1
        elif point < 1:
            binary_code += "0"
        else:
            binary_code += "1"
            break

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

    decoded_sequence = ""
    for _ in range(sequence_length):
        for j in range(len(unity)):
            if unity[j][1] <= point < unity[j][2]:
                prob_low = unity[j][1]
                prob_high = unity[j][2]
                diff = prob_high - prob_low
                decoded_sequence += unity[j][0]
                for k in range(len(unity)):
                    unity[k][1] = prob_low
                    unity[k][2] = probability[k] * diff + prob_low
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
            else:
                code += "1"
                if alphabet[i] == tree[j][1]:
                    break
        symbol_code.append([alphabet[i], code])

    encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
    return [encode, symbol_code], encode


def decode_ch(encoded_sequence):
    encode, symbol_code = encoded_sequence
    encode = list(encode)
    sequence = ""
    count = 0
    flag = 0

    i = 0
    while i < len(encode):
        for j in range(len(symbol_code)):
            if encode[i] == symbol_code[j][1]:
                sequence += symbol_code[j][0]
                flag = 1
                break
        if flag == 1:
            flag = 0
            i += 1
        else:
            count += 1
            if count == len(encode):
                break
            encode[i] = encode[i] + encode[i + 1]
            encode.pop(i + 1)

    return sequence


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
        probability = {symbol: count / 100 for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())

        encoded_data_ac, encoded_sequence_ac = encode_ac(unique_chars, probability, sequence_alphabet_size, sequence)
        bps_ac = len(encoded_sequence_ac) / sequence_length
        decoded_ac = decode_ac(encoded_data_ac, sequence_length)

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

print(
    "Практична робота виконана. Результати збережено в 'results_AC_CH.txt' та 'Результати стиснення методами АС та СН.png'.")