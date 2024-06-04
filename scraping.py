import os
import requests
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class DetikScraper():
    def __init__(self, topic):
        self.topic = topic

    def extract_html_files(self):
        # Create directory for HTML files if it doesn't exist
        if not os.path.exists(f'html/{self.topic}'):
            os.makedirs(f'html/{self.topic}')

        # Read the URL list file
        with open(f"urls/list-{self.topic}.txt", 'r') as f:
            for index, news_link in enumerate(f, start=1):
                news_link = news_link.strip()
                try:
                    # Extract HTML content from the news link
                    response = requests.get(news_link)
                    if response.status_code == 200:
                        # Save HTML content to a file with sequential filename
                        filename = f'html/{self.topic}/{index}.html'
                        with open(filename, 'wb') as html_file:
                            html_file.write(response.content)
                        print(f"File {filename} telah disimpan.")
                except Exception as e:
                    print(f"Error saat mengunduh {news_link}: {e}")

if __name__ == "__main__":
    topic = "berita"

    # Buat objek DetikScraper
    detik_scraper = DetikScraper(topic)
    detik_scraper.extract_html_files()