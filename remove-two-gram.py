import os

# Fungsi untuk membaca kamus dari file dengan format frekuensi1,kata1
def read_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                # Ambil bagian frekuensi dan kata
                frequency = line.split()[-1]  # Ambil data di bagian akhir
                word = line[:-len(frequency)].strip()  # Ambil sisa sebagai kata
                dictionary[word] = float(frequency)
            else:
                print("Error: Empty line found.")
    return dictionary

# Fungsi untuk menghapus duplikasi kata berdasarkan observasi eliminasi rasio
def remove_duplicates(dictionary_A, dictionary_B, threshold):
    unique_A = {}
    unique_B = {}

    for word, freq_A in dictionary_A.items():
        freq_B = dictionary_B.get(word, 0)

        # Hitung nilai rasio
        max_freq = max(freq_A, freq_B)
        min_freq = min(freq_A, freq_B)
        ratio = min_freq / max_freq if max_freq != 0 else 0

        # Hapus kata duplikat berdasarkan threshold
        if ratio < threshold:
            if freq_A >= freq_B:
                unique_A[word] = freq_A
            else:
                unique_B[word] = freq_B

    return unique_A, unique_B

# Fungsi untuk menyimpan kamus ke file
def save_dictionary(dictionary, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        # Urutkan kamus berdasarkan frekuensi dari yang terbesar ke terkecil
        sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        for word, frequency in sorted_dict:
            freq_str = str(int(frequency)) if frequency.is_integer() else f"{frequency:.1f}"
            file.write(f"{freq_str}\t{word}\n")

# Path ke kamus berita dan sepakbola
path_news = 'kamus/two-gram/berita_txts.txt'
path_football = 'kamus/two-gram/sepakbola_txts.txt'

# Baca kamus berita dan sepakbola
dict_news = read_dictionary(path_news)
dict_football = read_dictionary(path_football)

# Threshold untuk observasi eliminasi rasio
threshold_1 = 0.50
threshold_2 = 0.55

# Hapus duplikasi kata berdasarkan threshold
unique_news_1, unique_football_1 = remove_duplicates(dict_news, dict_football, threshold_1)
unique_news_2, unique_football_2 = remove_duplicates(dict_news, dict_football, threshold_2)

# Simpan kamus yang telah dihapus duplikasinya
output_news_1 = 'kamus_distinct/berita/two-gram_unique_50.txt'
output_football_1 = 'kamus_distinct/sepakbola/two-gram_unique_50.txt'
output_news_2 = 'kamus_distinct/berita/two-gram_unique_55.txt'
output_football_2 = 'kamus_distinct/sepakbola/two-gram_unique_55.txt'

save_dictionary(unique_news_1, output_news_1)
save_dictionary(unique_football_1, output_football_1)
save_dictionary(unique_news_2, output_news_2)
save_dictionary(unique_football_2, output_football_2)

print("Penghapusan duplikasi selesai.")