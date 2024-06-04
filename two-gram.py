import os
import re
from collections import Counter

# Fungsi untuk membaca teks dari file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Fungsi untuk menghitung frekuensi dua gram dalam teks
def count_two_grams(text):
    # Memisahkan teks menjadi kalimat-kalimat
    sentences = re.split(r'[\.\?!]', text)
    two_grams = []
    for sentence in sentences:
        # Memisahkan setiap kalimat menjadi kata-kata
        words = sentence.strip().lower().split()
        # Membuat dua gram dari kata-kata dalam setiap kalimat
        for i in range(len(words)-1):
            two_grams.append(f"{words[i]} {words[i+1]}")
    return Counter(two_grams)

# Fungsi untuk menyimpan kamus dua gram ke file
def save_two_gram(kamus, output_file):
    # Pastikan direktori untuk output_file ada
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count in sorted(kamus.items(), key=lambda item: item[1], reverse=True):
            file.write(f"{word.ljust(30)}{str(count).rjust(10)}\n")

# Direktori input (tempat file teks disimpan)
input_directory = 'preprocessing/'

# List kategori yang ingin diproses
categories = ['berita_txts', 'sepakbola_txts']

# Loop untuk setiap kategori
for category in categories:
    input_category_directory = os.path.join(input_directory, category)
    output_file = f'kamus/two-gram/{category}.txt'

    # Membuat kamus dua gram dari file-file 1-3000 dalam setiap kategori
    kamus_two_gram = Counter()
    for i, filename in enumerate(sorted(os.listdir(input_category_directory))):
        if i >= 3000:
            break
        file_path = os.path.join(input_category_directory, filename)
        text = read_text_file(file_path)
        kamus_two_gram.update(count_two_grams(text))

    # Menyimpan kamus dua gram ke file
    save_two_gram(kamus_two_gram, output_file)

    print(f"Pembuatan kamus dua gram untuk kategori {category} selesai!")

print("Semua pembuatan kamus dua gram telah selesai!")