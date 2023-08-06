from requests import Session
from lxml import html

_session = Session()


def search_articles(name, pages=1):
    search_urls = [f'http://weixin.sogou.com/weixin?type=2&query={name}&page={page}' for page in range(1, pages + 1)]
    xpath = '//*[@class="news-list"]/li'
    articles = []
    for search_url in search_urls:
        html_tree = _get_html(search_url)
        article_nodes = html_tree.xpath(xpath)
        for article_node in article_nodes:
            article_url = article_node.xpath('./div[2]/h3/a/@href')[0]
            official_url = article_node.xpath('./div[2]/div/a/@href')[0]
            digest = article_node.xpath('./div[2]/p')[0].text_content()
            articles.append(Article(article_url, official_url, digest))
    return articles


def search_officials(name, pages=1):
    pass


def get_official(id):
    pass


def _get_html(url):
    pass


def _identify_captcha():
    pass


def _identifying(captcha_image):
    pass
