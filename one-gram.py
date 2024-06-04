import os
import re
from collections import Counter

# Fungsi untuk membaca teks dari file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Fungsi untuk menghitung frekuensi satu gram dalam teks
def count_one_grams(text):
    # Memisahkan teks menjadi kata-kata dalam kalimat
    sentences = re.split(r'[\.\?!]', text)
    words = [re.findall(r'\b\w+\b', sentence.lower()) for sentence in sentences]
    # Menggabungkan semua kata-kata menjadi satu daftar satu gram
    one_grams = [word for sentence_words in words for word in sentence_words]
    return Counter(one_grams)

# Fungsi untuk menyimpan kamus satu gram ke file
def save_one_gram(kamus, output_file):
    # Pastikan direktori untuk output_file ada
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count in sorted(kamus.items(), key=lambda item: item[1], reverse=True):
            file.write(f"{word.ljust(20)}{str(count).rjust(10)}\n")

# Direktori input (tempat file teks disimpan)
input_directory = 'preprocessing/'

# List kategori yang ingin diproses
categories = ['berita_txts', 'sepakbola_txts']

# Loop untuk setiap kategori
for category in categories:
    input_category_directory = os.path.join(input_directory, category)
    output_file = f'kamus/one-gram/{category}.txt'

    # Membuat kamus satu gram dari file-file 1-3000 dalam setiap kategori
    kamus_one_gram = Counter()
    for i, filename in enumerate(sorted(os.listdir(input_category_directory))):
        if i >= 3000:
            break
        file_path = os.path.join(input_category_directory, filename)
        text = read_text_file(file_path)
        kamus_one_gram.update(count_one_grams(text))

    # Menyimpan kamus satu gram ke file
    save_one_gram(kamus_one_gram, output_file)

    print(f"Pembuatan kamus satu gram untuk kategori {category} selesai!")

print("Semua pembuatan kamus satu gram telah selesai!")