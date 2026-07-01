import feedparser
from urllib.parse import quote


def fetch_stock_news(company_name, max_items=5):

    query = quote(company_name)
    url = f"https://news.google.com/rss/search?q={query}&hl=ja&gl=JP&ceid=JP:ja"

    feed = feedparser.parse(url)

    news = []
    for entry in feed.entries[:max_items]:
        news.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
        })

    return news
