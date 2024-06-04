import os
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor

# Initialize logging
logging.basicConfig(level=logging.INFO)

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory '{path}' successfully created")
    except OSError as error:
        logging.error(f"Error creating directory '{path}': {error}")

def extract_content_from_html(filepath):
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None, None

    try:
        with open(filepath, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            title = soup.find('title')
            paragraphs = soup.find_all('p')

            if not title or not paragraphs:
                logging.warning(f"Missing elements in file: {filepath}")
                return None, None

            title_text = title.text.strip()
            # Filter out unwanted content
            filtered_paragraphs = []
            for p in paragraphs:
                paragraph_text = p.text.strip()
                if paragraph_text and not paragraph_text.startswith(('ADVERTISEMENT', 'SCROLL TO CONTINUE', 'Artikel ini telah tayang di detikSport.', '[Gambas:Twitter]', 'Artikel ini telah tayang di detikSport dengan judul', 'Baca selengkapnya di sini.')):
                    filtered_paragraphs.append(paragraph_text)
            content = '\n'.join(filtered_paragraphs)
            return title_text, content
    except Exception as e:
        logging.error(f"Error processing file '{filepath}': {e}")
        return None, None

def convert_html_to_txt(html_directory, txt_directory, category, filename):
    html_path = os.path.join(html_directory, filename)
    txt_path = os.path.join(txt_directory, filename.replace('.html', '.txt'))

    if os.path.exists(txt_path):
        logging.info(f"File already converted: {txt_path}")
        return

    title, content = extract_content_from_html(html_path)
    if title and content:
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(f"Title: {title}\n\nContent:\n{content}\n")
            logging.info(f"Converted and saved: {txt_path}")

def process_category(html_dir, txt_dir, category):
    output_dir = os.path.join('extract_content', txt_dir)
    create_directory(output_dir)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for file in os.listdir(html_dir):
            if file.endswith('.html'):
                future = executor.submit(convert_html_to_txt, html_dir, output_dir, category, file)
                futures.append(future)
        
        for future in futures:
            future.result()

    logging.info(f"Conversion for category '{category}' completed!")

# Directories and Categories
BASE_HTML_DIR = 'html'
categories = {
    'sepakbola': ('sepakbola', 'sepakbola_txts'),
    'berita': ('berita', 'berita_txts')
}

def main():
    # Process each category
    for category, (html_dir, txt_dir) in categories.items():
        logging.info(f"Starting conversion for category '{category}'...")
        process_category(os.path.join(BASE_HTML_DIR, html_dir), txt_dir, category)

if __name__ == "__main__":
    main()