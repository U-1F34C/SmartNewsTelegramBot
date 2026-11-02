# Загрузка необходимых библиотек
import csv
from pathlib import Path
import asyncio

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://habr.com/ru/news/"  # URL для парсинга новостей
NEWS_FILE = Path(__file__).resolve().parent / "news.csv"

# Функция для получения последней новости из CSV-файла
# return: {"status": bool, "message": str, "data": {"id": id, "title": title, "link": link, "description": description}}
async def get_news():
    try:
        with NEWS_FILE.open(mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            try:
                news = next(reader)
            except StopIteration:
                return {"status": False, "message": "No news available", "data": None}
            return {"status": True, "message": "Success", "data": news}
    except FileNotFoundError:
        return {"status": False, "message": "No news available", "data": None}
    except OSError as exc:
        return {"status": False, "message": f"Failed to read news file: {exc}", "data": None}

# Функция для парсинга новостей с сайта и сохранения их в CSV-файл
# return: {"status": bool, "message": str, "data": {"id": id, "title": title, "link": link, "description": description}}
async def parse_news():
    response = requests.get(URL)

    if response.status_code != 200:
        return {"status": False, "message": f"Connection failed with status code: {response.status_code}", "data": None}

    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.find("article", class_="tm-articles-list__item")

    if news is None:
        return {"status": False, "message": "No news found on the page", "data": None}

    old_news = await get_news()
    if old_news["status"] and old_news["data"]:
        old_id = old_news["data"].get("\ufeffid") or old_news["data"].get("id")
        if news.get("id") == old_id:
            return {"status": True, "message": "No new news available", "data": old_news["data"]}

    article_id = news.get("id")
    title = news.find("h2", class_="tm-title").text.strip()
    link = f"https://habr.com{news.find('a', class_='tm-title__link').get('href')}"
    description = BeautifulSoup(requests.get(link).text, "html.parser").find(
        "div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2"
    ).p.text.strip()

    news_list = {"id": article_id, "title": title, "link": link, "description": description}

    df = pd.DataFrame([news_list])

    try:
        df.to_csv(NEWS_FILE, index=False, encoding="utf-8-sig")
        return {"status": True, "message": "Success", "data": news_list}
    except Exception as exc:
        return {"status": False, "message": f"Error occurred while saving CSV: {exc}", "data": None}


if __name__ == "__main__":
    asyncio.run(parse_news())