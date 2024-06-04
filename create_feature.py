import os
import re
import random
from collections import Counter

# Fungsi untuk membersihkan teks
def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

# Fungsi untuk membaca daftar stopwords dari file eksternal
def read_stopwords(file_path):
    stopwords = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if word:
                stopwords.add(word)
    return stopwords

# Fungsi untuk menghitung jumlah kata dalam teks (tidak termasuk stopwords)
def count_words(text, stopwords):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return len(filtered_words)

# Fungsi untuk menghitung fitur untuk bagian judul
def calculate_title_feature(title, dictionary, stopwords):
    title_words = clean_text(title).split()
    total_title_words = count_words(title, stopwords)
    word_counter = Counter(title_words)
    feature = sum(word_counter[word] for word in word_counter if word in dictionary)
    return feature / total_title_words if total_title_words > 0 else 0

# Fungsi untuk menghitung fitur untuk bagian konten (bagian atas, tengah, atau bawah)
def calculate_content_feature(content, dictionary, weight, stopwords):
    content_words = clean_text(content).split()
    total_content_words = count_words(content, stopwords)
    word_counter = Counter(content_words)
    feature = sum(word_counter[word] for word in word_counter if word in dictionary)
    return weight * feature / total_content_words if total_content_words > 0 else 0

# Fungsi untuk menghitung semua fitur untuk satu halaman web
def calculate_all_features(title, content_top, content_middle, content_bottom, dictionaries, weights, stopwords):
    features = []
    for category_dict, weight in zip(dictionaries, weights):
        category_features = []
        for dictionary in category_dict:
            title_feature = calculate_title_feature(title, dictionary, stopwords)
            top_feature = calculate_content_feature(content_top, dictionary, weight[0], stopwords)
            middle_feature = calculate_content_feature(content_middle, dictionary, weight[1], stopwords)
            bottom_feature = calculate_content_feature(content_bottom, dictionary, weight[2], stopwords)
            category_features.extend([title_feature, top_feature, middle_feature, bottom_feature])
        features.extend(category_features)
    return features

# Direktori tempat menyimpan file teks
directories = [r"content_splitting/berita", r"content_splitting/sepakbola"]

# Kamus-kamus untuk setiap kategori (1-kata, 2-kata, dan 3-kata)
positive_dictionaries = [
    [
        "kamus_distinct/berita/one-gram_unique_55.txt", 
        "kamus_distinct/berita/two-gram_unique_55.txt", 
        "kamus_distinct/berita/three-gram_unique_55.txt"
    ],
    [
        "kamus_distinct/sepakbola/one-gram_unique_55.txt", 
        "kamus_distinct/sepakbola/two-gram_unique_55.txt", 
        "kamus_distinct/sepakbola/three-gram_unique_55.txt"
    ]
]

# Bobot untuk bagian konten (bagian atas, tengah, dan bawah)
weights = [(0.5, 0.4, 0.3), (0.5, 0.4, 0.3)]

# Mendefinisikan path untuk file stopwords
stopwords_path = "stopword.txt"
# Membaca stopwords dari file eksternal
stopwords = read_stopwords(stopwords_path)

# Menyimpan data fitur dan label
data = {0: [], 1: []}  # 0 untuk berita, 1 untuk sepak bola

# Proses setiap folder
for label, directory in enumerate(directories):
    # Mendapatkan daftar file dalam direktori
    txt_files = [file for file in os.listdir(directory) if file.endswith(".dat")]

    # Filter file yang memiliki urutan lebih dari 3000
    txt_files = [file for file in txt_files if int(re.findall(r'\d+', file)[0]) > 3000]

    # Proses setiap file teks
    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            # Pisahkan teks menjadi bagian judul, atas, tengah, dan bawah (masing-masing 30%, 40%, 30%)
            content_words = content.split()
            total_content_words = len(content_words)
            top_end = int(total_content_words * 0.3)
            middle_start = int(total_content_words * 0.3)
            middle_end = int(total_content_words * 0.7)
            title = " ".join(content_words[:top_end])
            content_top = " ".join(content_words[:top_end])
            content_middle = " ".join(content_words[middle_start:middle_end])
            content_bottom = " ".join(content_words[middle_end:])

            # Menghitung fitur untuk setiap halaman web
            features = calculate_all_features(title, content_top, content_middle, content_bottom, positive_dictionaries, weights, stopwords)

            # Simpan fitur dan label ke dalam data
            data[label].append(features)

# Pembagian data menjadi training set (80%) dan testing set (20%)
training_data = []
testing_data = []

for label in data:
    # Acak data
    random.shuffle(data[label])
    # Hitung jumlah data untuk training set
    train_size = int(len(data[label]) * 0.8)
    # Pisahkan data
    training_data.extend([(features, label) for features in data[label][:train_size]])
    testing_data.extend([(features, label) for features in data[label][train_size:]])

# Gabungkan data training dan testing ke dalam satu file CSV
combined_data = training_data + testing_data

def save_to_csv(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        for features, label in data:
            file.write(",".join(map(str, features)) + "," + str(label) + "\n")

save_to_csv("combined_features.csv", combined_data)
save_to_csv("training_features.csv", training_data)
save_to_csv("testing_features.csv", testing_data)

print("Features extracted and saved to CSV files.")