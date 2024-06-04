import os

def split_content(content):
    lines = content.split('\n')
    total_lines = len(lines)
    third = total_lines // 3

    atas = "\n".join(lines[:third])
    tengah = "\n".join(lines[third:2*third])
    bawah = "\n".join(lines[2*third:])

    return atas, tengah, bawah

def process_text_file(file_path, output_directory, category):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    title = ""
    content = ""
    is_title = True

    for line in lines:
        if line.strip() == "":
            is_title = False
            continue
        if is_title:
            title = line.strip()
            is_title = False
        elif "Content:" not in line:
            content += line.strip() + "\n"

    atas, tengah, bawah = split_content(content)

    output_category_directory = os.path.join(output_directory, category)
    if not os.path.exists(output_category_directory):
        os.makedirs(output_category_directory)

    output_filename = os.path.splitext(os.path.basename(file_path))[0] + ".clean.dat"
    output_filepath = os.path.join(output_category_directory, output_filename)

    with open(output_filepath, "w", encoding="utf-8") as text_file:
        text_file.write(f"{title}\n\n<atas>\n{atas}\n</atas>\n\n<tengah>\n{tengah}\n</tengah>\n\n<bawah>\n{bawah}</bawah>")

# Ganti dengan path direktori tempat Anda ingin menyimpan file yang telah dipisah
output_directory = "content_splitting"

# Membuat direktori output jika belum ada
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Direktori tempat file txt berada, beserta kategorinya
txt_directories = {
    "extract_content/sepakbola_txts": "sepakbola",
    "extract_content/berita_txts": "berita"
}

# Loop melalui semua file dalam direktori
for txt_directory, category in txt_directories.items():
    for filename in os.listdir(txt_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(txt_directory, filename)
            process_text_file(file_path, output_directory, category)