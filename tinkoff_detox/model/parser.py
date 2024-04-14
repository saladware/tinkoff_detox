from httpx import Client
import re


def get_comments_by_article(path: str):
    client = Client()

    res = client.get(f"https://journal.tinkoff.ru/{path}")

    regexp = re.compile(r'{"articleId":*([^,]+)*,')

    uuid = regexp.findall(res.text)[0][1:-1]

    res = client.get(f"https://social.journal.tinkoff.ru/api/v20/comments/?uuid={uuid}&unsafe=true")

    return [comment["text"] for comment in res.json()["data"]]


print(get_comments_by_article("news/otsrochka-ot-armii-po-uchebe/"))
