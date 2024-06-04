import os
import re

# Fungsi untuk melakukan preprocessing teks
def preprocess_text(text):
    # Hapus tanda baca selain titik (.) dan hapus spasi ganda
    text = re.sub(r'[^\w\s.]', '', text)
    text = re.sub(r'\s+', ' ', text)  # Hapus spasi ganda

    # Hapus kata "Title:" dan "Content:" serta spasi ganda setelahnya
    text = re.sub(r'\bTitle:\s*', '', text)
    text = re.sub(r'\bContent:\s*', '\n', text)  # Pisahkan konten dari judul dengan baris baru

    return text.strip()  # Hapus whitespace di awal dan akhir

# Fungsi untuk melakukan preprocessing dan menyimpan ke direktori preprocessing
def preprocessing(input_dir, output_dir):
    for category in os.listdir(input_dir):
        category_input_dir = os.path.join(input_dir, category)
        category_output_dir = os.path.join(output_dir, category)
        if not os.path.exists(category_output_dir):
            os.makedirs(category_output_dir)
        
        for filename in os.listdir(category_input_dir):
            input_filepath = os.path.join(category_input_dir, filename)
            output_filepath = os.path.join(category_output_dir, filename)
            with open(input_filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                # Menghapus "title:" dan "content:" dari teks
                text = re.sub(r'title:|content:', '', text, flags=re.IGNORECASE)
                # Hapus tanda baca selain titik (.) dan spasi ganda
                text = re.sub(r'[^\w\s.]', '', text)
                text = re.sub(r'\s+', ' ', text)
                # Ubah teks ke lower case
                text = text.lower()
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(text)

# Path ke direktori utama
input_dir = "extract_content"
output_dir = "preprocessing"

# Lakukan preprocessing
preprocessing(input_dir, output_dir)

print("Preprocessing selesai.")