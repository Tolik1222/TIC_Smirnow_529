import math
import collections
import matplotlib.pyplot as plt

with open("sequence.txt", "r", encoding="utf-8") as file:
    sequences = file.read().strip().split(",")

if len(sequences) != 8:
    raise ValueError(f"Помилка: Очікується 8 послідовностей, отримано {len(sequences)}")

for i, seq in enumerate(sequences, 1):
    if len(seq) != 100:
        raise ValueError(f"Помилка: Послідовність {i} має довжину {len(seq)} замість 100")


def encode_rle(sequence):
    encoded = []
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            encoded.append((sequence[i - 1], count))
            count = 1
    encoded.append((sequence[-1], count))  # Додаємо останній символ

    encoded_str = "".join(f"{count}{char}" for char, count in encoded)
    return encoded_str, encoded


def decode_rle(encoded_list):
    return "".join(char * count for char, count in encoded_list)


def encode_lzw(sequence):
    dictionary = {chr(i): i for i in range(65536)}
    result = []
    current = ""
    size = 0
    lzw_steps = []

    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            element_bits = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
            lzw_steps.append(f"Code: {dictionary[current]}, Element: {current}, Bits: {element_bits}")
            result.append(dictionary[current])
            size += element_bits
            dictionary[new_str] = len(dictionary)
            current = c

    if current:
        last = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
        lzw_steps.append(f"Code: {dictionary[current]}, Element: {current}, Bits: {last}")
        result.append(dictionary[current])
        size += last

    return result, size, lzw_steps


def decode_lzw(sequences):
    dictionary = {i: chr(i) for i in range(65536)}
    results = ""
    previous = None
    current = ""

    for code in sequences:
        if code in dictionary:
            current = dictionary[code]
            results += current
            if previous is not None:
                dictionary[len(dictionary)] = previous + current[0]
            previous = current
        else:
            current = previous + previous[0]
            results += current
            dictionary[len(dictionary)] = current
            previous = current

    return result



results = []
with open("results_rle_lzw.txt", "w", encoding="utf-8") as file:
    file.write(" РЕЗУЛЬТАТИ СТИСКАННЯ ПОСЛІДОВНОСТЕЙ \n")
    file.write("=" * 80 + "\n\n")

    for idx, seq in enumerate(sequences, 1):
        file.write(f" Послідовність {idx}\n")
        file.write("-" * 80 + "\n")
        file.write(f"Оригінальна послідовність:\n{seq}\n\n")

        freqs = collections.Counter(seq)
        entropy = -sum((count / 100) * math.log2(count / 100) for count in freqs.values())
        file.write(f" Ентропія: {entropy:.2f}\n\n")

        file.write("RLE Кодування\n")
        rle_encoded, rle_list = encode_rle(seq)
        rle_decoded = decode_rle(rle_list)
        rle_size_bits = sum(len(bin(count)[2:]) + 8 for _, count in rle_list)
        rle_compression_ratio = round(len(seq) / len(rle_encoded), 2) if len(rle_encoded) < len(seq) else "1.0"

        file.write(f"Закодована послідовність (RLE):\n{rle_encoded}\n")
        file.write(f"Розмір RLE: {rle_size_bits} bits\n")
        file.write(f"Декодована послідовність (перевірка):\n{rle_decoded}\n")
        file.write(f" Коефіцієнт стиснення RLE: {rle_compression_ratio}\n\n")

        file.write(" LZW Кодування \n")
        lzw_encoded, lzw_size, lzw_steps = encode_lzw(seq)
        lzw_decoded = decode_lzw(lzw_encoded)
        lzw_compression_ratio = round((len(seq) * 16) / lzw_size, 2)

        file.write(" Таблиця кодування LZW:\n")
        file.write("-" * 40 + "\n")
        file.write(f"{'Код':<10}{'Елемент':<15}{'Біти'}\n")
        file.write("-" * 40 + "\n")
        for step in lzw_steps:
            file.write(step + "\n")
        file.write("-" * 40 + "\n")

        file.write(f"Закодована послідовність (LZW):\n{','.join(map(str, lzw_encoded))}\n")
        file.write(f"Розмір LZW: {lzw_size} bits\n")
        file.write(f"Декодована послідовність (перевірка):\n{lzw_decoded}\n")
        file.write(f" Коефіцієнт стиснення LZW: {lzw_compression_ratio}\n")

        file.write("\n" + "=" * 80 + "\n\n")

        results.append([f"{entropy:.2f}", str(rle_compression_ratio), f"{lzw_compression_ratio}"])


print("Файл results_rle_lzw.txt успішно створено!")

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
headers = ['Ентропія', 'КС RLE', 'КС LZW']
rows = [f"Послідовність {i + 1}" for i in range(len(sequences))]
table = ax.table(cellText=results, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')
table.set_fontsize(12)
table.scale(1, 2)
plt.savefig("Результати_стиснення.png", bbox_inches='tight')
print("Файл Результати_стиснення.png успішно створено!")
