import os
import re
from collections import Counter

# Fungsi untuk membaca teks dari file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Fungsi untuk membersihkan teks dari tanda baca
def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

# Fungsi untuk menghitung frekuensi tiga gram dalam teks
def count_three_grams(text):
    # Menghapus tanda baca dari teks
    cleaned_text = clean_text(text)
    # Memisahkan teks menjadi kalimat-kalimat
    sentences = re.split(r'[\.\?!]', cleaned_text)
    three_grams = []
    for sentence in sentences:
        # Memisahkan setiap kalimat menjadi kata-kata
        words = sentence.strip().lower().split()
        # Membuat tiga gram dari kata-kata dalam setiap kalimat
        for i in range(len(words)-2):
            three_grams.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    return Counter(three_grams)

# Fungsi untuk menyimpan kamus tiga gram ke file
def save_three_gram(kamus, output_file):
    # Pastikan direktori untuk output_file ada
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count in sorted(kamus.items(), key=lambda item: item[1], reverse=True):
            file.write(f"{word.ljust(40)}{str(count).rjust(10)}\n")

# Direktori input (tempat file teks disimpan)
input_directory = 'preprocessing/'

# List kategori yang ingin diproses
categories = ['berita_txts', 'sepakbola_txts']

# Loop untuk setiap kategori
for category in categories:
    input_category_directory = os.path.join(input_directory, category)
    output_file = f'kamus/three-gram/{category}.txt'

    # Membuat kamus tiga gram dari file-file 1-3000 dalam setiap kategori
    kamus_three_gram = Counter()
    for i, filename in enumerate(sorted(os.listdir(input_category_directory))):
        if i >= 3000:
            break
        file_path = os.path.join(input_category_directory, filename)
        text = read_text_file(file_path)
        kamus_three_gram.update(count_three_grams(text))

    # Menyimpan kamus tiga gram ke file
    save_three_gram(kamus_three_gram, output_file)

    print(f"Pembuatan kamus tiga gram untuk kategori {category} selesai!")

print("Semua pembuatan kamus tiga gram telah selesai!")