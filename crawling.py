import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timedelta

class DetikCrawler():
    def __init__(self, topic, num_of_data):
        self.topic = topic
        self.num_of_data = num_of_data

    def get_urls(self):
        news_links = set()  # Menggunakan set untuk menyimpan tautan unik
        page = 1
        while len(news_links) < self.num_of_data:
            url = f"https://www.detik.com/search/searchall?query={self.topic}&siteid=2&sortby=time&page={page}"
            html_page = requests.get(url).content
            soup = BeautifulSoup(html_page, 'html.parser')
            articles = soup.find_all('article')

            if not articles:
                break

            for article in articles:
                urls = article.find_all('a')
                for url in urls:
                    news_link = url.get('href')
                    if self.is_topic_related(news_link):
                        news_links.add(news_link)
                        print(f"Mengambil tautan: {news_link}")

            page += 1

        return news_links

    def is_topic_related(self, news_link):
        # Pemeriksaan apakah tautan terkait dengan topik
        return self.topic.lower() in news_link.lower()

    def create_url_file(self):
        # Create directory for URLs if it doesn't exist
        if not os.path.exists('urls'):
            os.makedirs('urls')

        # Create or overwrite the URL list file for the topic
        with open(f"urls/list-{self.topic}.txt", 'w') as f:
            for news_link in self.get_urls():
                f.write(news_link + '\n')
        print(f"File list-{self.topic}.txt telah dibuat di folder 'urls'.")

if __name__ == "__main__":
    topic = "berita"
    num_of_data = 4201

    # Buat objek DetikCrawler dengan jumlah data yang ditentukan
    detik_crawler = DetikCrawler(topic, num_of_data)
    detik_crawler.create_url_file()