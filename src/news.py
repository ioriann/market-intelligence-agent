import feedparser
from urllib.parse import quote
import urllib.request
import urllib.error
import socket

def fetch_stock_news(company_name, max_items=5):

    query = quote(company_name)
    url = f"https://news.google.com/rss/search?q={query}&hl=ja&gl=JP&ceid=JP:ja"

    # 10秒間応答がなければタイムアウト
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            # HTTPステータスコードが200以外の場合は例外を発生させる
            feed = feedparser.parse(response)
            if response.status != 200:
                print(f"HTTP Error: {response.status}")
                news = []
                return news
    
    except urllib.error.URLError as e:
        # 失敗した具体的な理由を表示する
        if isinstance(e.reason, socket.timeout):
            print("Request timed out")
            news = []
            return news
        else:
            print(f"Failed to fetch news: {e.reason}")
            news = []
            return news

    news = []
    for entry in feed.entries[:max_items]:
        news.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
        })

    return news
