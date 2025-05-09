"""
<div class="tm-articles-list" data-test-id="articles-list">
article
<h2 class="tm-title tm-title_h2" data-test-id="articleTitle"><!--[--><a href="/ru/articles/908020/" class="tm-title__link" data-article-link="true" data-test-id="article-snippet-title-link"><span>Что происходит, когда мы вводим в браузер имя сайта и нажимаем enter?</span></a><!--]--></h2>
<time datetime="2025-05-08T17:52:01.000Z" title="2025-05-08, 20:52">24 минуты назад</time>

"""
from pprint import pprint
import re
import bs4
import requests
from fake_headers import Headers

keywords = [
    "интеллект",
    "история"
    "Код",
    "Хабр",
    "GPT",
    "баг",
    "linux"
]

keywords = [i.lower() for i in keywords]


def generate_headers():

    headers = Headers(os='win', browser='chrome').generate()

    return headers


response = requests.get("https://habr.com/ru/articles/", headers=generate_headers())

main_html = response.text

main_page_soup = bs4.BeautifulSoup(main_html, features="lxml")

tm_articles_list_tag = main_page_soup.find("div", class_ = "tm-articles-list")

article_tags = tm_articles_list_tag.find_all("article")

parsed_articles_list = []

for article_tag in article_tags:

    h2_tag = article_tag.find("h2")
    a_tag = h2_tag.find("a")
    time_tag = article_tag.find("time")

    header = h2_tag.text
    pattern = r"[.,:;!?—–\-–«»\"\'\[\]\(\)]"
    pre_final_header = re.sub(pattern, "", header)
    pattern2 = r"…"
    final_header = re.sub(pattern2, "", pre_final_header)



    link = a_tag["href"]
    full_link = f"https://habr.com{link}"
    published_time = time_tag["datetime"]


    for word in final_header.split():
        if word.lower() in keywords:
            parsed_article = {
                "дата": published_time,
                "заголовок": header,
                "ссылка": full_link
            }

            parsed_articles_list.append(parsed_article)
            break


pprint(parsed_articles_list)






