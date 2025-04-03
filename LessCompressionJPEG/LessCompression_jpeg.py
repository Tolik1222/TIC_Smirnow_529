import numpy as np
import math
from scipy import fftpack
from PIL import Image
import os
import struct

QUANTIZATION_TABLE_1 = np.array([
    [80, 64, 100, 156, 200, 184, 248, 272],
    [72, 84, 116, 164, 224, 260, 280, 244],
    [96, 108, 144, 208, 256, 312, 340, 288],
    [124, 140, 172, 240, 308, 368, 400, 352],
    [160, 196, 248, 316, 376, 440, 468, 408],
    [232, 280, 340, 388, 448, 500, 520, 480],
    [328, 384, 432, 464, 508, 540, 560, 528],
    [420, 480, 500, 520, 552, 568, 580, 560]
])

QUANTIZATION_TABLE_2 = np.array([
    [120, 100, 140, 200, 260, 240, 320, 360],
    [112, 128, 160, 220, 280, 340, 380, 328],
    [140, 152, 192, 260, 320, 380, 420, 360],
    [180, 200, 240, 300, 380, 440, 480, 420],
    [240, 280, 340, 400, 460, 520, 560, 500],
    [320, 380, 440, 480, 540, 580, 600, 560],
    [400, 460, 500, 540, 580, 620, 640, 600],
    [480, 540, 560, 580, 620, 640, 660, 640]
])


def rgb_to_ycbcr(image):
    rgb = np.array(image, dtype=float)
    ycbcr = np.zeros_like(rgb)
    ycbcr[:, :, 0] = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]  # Y
    ycbcr[:, :, 1] = -0.168736 * rgb[:, :, 0] - 0.331264 * rgb[:, :, 1] + 0.5 * rgb[:, :, 2] + 128  # Cb
    ycbcr[:, :, 2] = 0.5 * rgb[:, :, 0] - 0.418688 * rgb[:, :, 1] - 0.081312 * rgb[:, :, 2] + 128  # Cr
    return np.clip(ycbcr, 0, 255)


def ycbcr_to_rgb(ycbcr):
    ycbcr = np.array(ycbcr, dtype=float)
    rgb = np.zeros_like(ycbcr)
    y = ycbcr[:, :, 0]
    cb = ycbcr[:, :, 1] - 128
    cr = ycbcr[:, :, 2] - 128
    rgb[:, :, 0] = y + 1.402 * cr  # R
    rgb[:, :, 1] = y - 0.344136 * cb - 0.714136 * cr  # G
    rgb[:, :, 2] = y + 1.772 * cb  # B
    return np.clip(rgb, 0, 255).astype(np.uint8)


def dct_2d(block):
    block = block - 128
    return fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')


def idct_2d(block):
    block = fftpack.idct(fftpack.idct(block.T, norm='ortho').T, norm='ortho')
    return block + 128


def quantize(block, q_table):
    return np.round(block / q_table).astype(int)


def dequantize(block, q_table):
    return block * q_table


def zigzag_scan(block):
    if block.shape != (8, 8):
        raise ValueError(f"Неправильний розмір блоку: {block.shape}. Очікується (8, 8).")
    zigzag = np.zeros(64, dtype=int)
    order = [
        (0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
        (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0

                                                                 , 5),
        (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
        (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
        (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
        (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
        (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
        (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)
    ]
    for k, (i, j) in enumerate(order):
        zigzag[k] = block[i, j]
    return zigzag


def zigzag_to_block(zigzag):
    block = np.zeros((8, 8), dtype=int)
    order = [
        (0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
        (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 5),
        (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
        (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
        (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
        (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
        (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
        (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)
    ]
    for k, (i, j) in enumerate(order):
        block[i, j] = zigzag[k]
    return block


def encode(input_file, output_file, q_table):
    #Кодування зображення у проміжний файл .asf
    try:
        input_image = Image.open(input_file).convert('RGB')
        input_size = os.path.getsize(input_file)
    except FileNotFoundError:
        print(f"Файл {input_file} не знайдено.")
        return None, None, None

    ycbcr = rgb_to_ycbcr(input_image)
    height, width = input_image.size[1], input_image.size[0]
    pad_height = (8 - height % 8) % 8
    pad_width = (8 - width % 8) % 8
    ycbcr = np.pad(ycbcr, ((0, pad_height), (0, pad_width), (0, 0)), mode='constant', constant_values=128)
    height, width = ycbcr.shape[0], ycbcr.shape[1]
    blocks_per_line = width // 8
    blocks_count = (height // 8) * blocks_per_line

    dc = np.zeros((blocks_count, 3), dtype=int)
    ac = np.zeros((blocks_count, 63, 3), dtype=int)

    for block_idx in range(blocks_count):
        i = (block_idx // blocks_per_line) * 8
        j = (block_idx % blocks_per_line) * 8
        for c in range(3):
            block = ycbcr[i:i + 8, j:j + 8, c]
            if block.shape != (8, 8):
                block = np.pad(block, ((0, 8 - block.shape[0]), (0, 8 - block.shape[1])), mode='constant',
                               constant_values=128)
            dct_block = dct_2d(block)
            quant_block = quantize(dct_block, q_table)
            zigzag = zigzag_scan(quant_block)
            dc[block_idx, c] = zigzag[0]
            ac[block_idx, :, c] = zigzag[1:]

    # Збереження у .asf
    with open(output_file, 'wb') as f:
        f.write(struct.pack('i', blocks_count))  # 4 байти на blocks_count
        f.write(struct.pack('i', height))  # 4 байти на висоту
        f.write(struct.pack('i', width))  # 4 байти на ширину
        for block_idx in range(blocks_count):
            for c in range(3):
                f.write(struct.pack('i', dc[block_idx, c]))
        for block_idx in range(blocks_count):
            for i in range(63):
                for c in range(3):
                    f.write(struct.pack('i', ac[block_idx, i, c]))

    return dc, ac, blocks_count


def decode_jpeg(dc, ac, blocks_count, q_table, output_filename):
    block_side = 8
    blocks_per_line = int(math.ceil(math.sqrt(blocks_count)))
    image_height = (blocks_count // blocks_per_line + (1 if blocks_count % blocks_per_line else 0)) * block_side
    image_width = blocks_per_line * block_side
    npmat = np.zeros((image_height, image_width, 3), dtype=np.float32)

    for block_idx in range(blocks_count):
        i = (block_idx // blocks_per_line) * block_side
        j = (block_idx % blocks_per_line) * block_side
        if i >= image_height or j >= image_width:
            continue
        for c in range(3):
            zigzag = np.concatenate([[dc[block_idx, c]], ac[block_idx, :, c]])
            quant_matrix = zigzag_to_block(zigzag)
            dct_matrix = dequantize(quant_matrix, q_table)
            block = idct_2d(dct_matrix)
            npmat[i:i + 8, j:j + 8, c] = block

    decoded_image = Image.fromarray(ycbcr_to_rgb(npmat), 'RGB')
    decoded_image.save(output_filename, quality=10)
    return decoded_image


def process_image(input_path, texture_name):
    try:
        input_size = os.path.getsize(input_path)
    except FileNotFoundError:
        print(f"Файл {input_path} не знайдено.")
        return []

    q_tables = [QUANTIZATION_TABLE_1, QUANTIZATION_TABLE_2]
    results = []
    os.makedirs("Results", exist_ok=True)

    for idx, q_table in enumerate(q_tables, 1):
        asf_filename = f"Results/{texture_name}_q{idx}.asf"
        jpeg_filename = f"Results/JPEG_{texture_name}_q{idx}.jpg"

        # Кодування у .asf
        dc, ac, blocks_count = encode(input_path, asf_filename, q_table)
        if dc is None:
            continue

        decoded_image = decode_jpeg(dc, ac, blocks_count, q_table, jpeg_filename)

        output_size = os.path.getsize(jpeg_filename)
        ratio = input_size / output_size
        width, height = decoded_image.size

        result = (
            f"Дані для {texture_name} (таблиця квантування {idx})\n"
            f"Розмір вихідного файла: {input_size} байт\n"
            f"Розмір файла JPEG: {output_size} байт\n"
            f"Розмір зображення JPEG: {width}x{height}\n"
            f"Коефіцієнт стиснення: {ratio:.2f}\n"
        )
        results.append(result)

    return results


def main():
    print("Введіть шляхи до трьох JPEG-файлів зі своєї директорії.")
    images = []
    texture_types = ["слаботекстурного зображення", "середньотекстурного зображення", "сильнотекстурного зображення"]

    for i, texture in enumerate(texture_types, 1):
        while True:
            input_path = input(f"Введіть шлях до {i}-го файлу ({texture}): ").strip()
            if os.path.exists(input_path) and input_path.lower().endswith('.jpg'):
                images.append((input_path, texture))
                break
            else:
                print("Файл не знайдено або не є JPEG. Спробуйте ще раз.")

    all_results = []
    for input_path, texture_name in images:
        results = process_image(input_path, texture_name)
        all_results.extend(results)

    with open("results_jpeg.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(all_results))
    print("Обробка завершена. Результати збережено в 'results_jpeg.txt'. Декодовані зображення — у папці 'Results'.")
    print("Очікується 6 декодованих зображень: по 2 для кожного вхідного зображення (q1 і q2).")


if __name__ == "__main__":
    main()