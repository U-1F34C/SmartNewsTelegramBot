import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

url = "https://habr.com/ru/news/"
news_list = []

def get_news():
    with open('news.csv', mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return next(reader)


def parse_news():
    response = requests.get(url)

    if response.status_code != 200:
        return "Connection failed with status code:", False, response.status_code

    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.find("article", class_="tm-articles-list__item")

    old_news = get_news()

    if news.get("id") == old_news['\ufeffid']:
        return old_news, False
    
    id = news.get("id")
    title = news.find("h2", class_="tm-title").text.strip()
    link = f"https://habr.com{news.find('a', class_='tm-title__link').get('href')}"
    description = BeautifulSoup(requests.get(link).text, "html.parser").find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2").p.text.strip()
    news_list.append({"id": id, "title": title, "link": link, "description": description})

    df = pd.DataFrame(news_list)

    try:
        df.to_csv("news.csv", index=False, encoding="utf-8-sig")
        return news_list, True
    except Exception as e:
        return "Error occurred while saving CSV:", False, e

if __name__ == "__main__":
    print(parse_news())