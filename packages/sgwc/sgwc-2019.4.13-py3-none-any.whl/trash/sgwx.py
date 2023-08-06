from trash.official_account import OfficialAccount
from requests import Session, utils
from tempfile import TemporaryFile
from trash.article import Article
from lxml import html
from PIL import Image


class S:
    def __init__(self):
        self._session = Session()

    def search_articles(self, name, pages=1):
        search_urls = [f'http://weixin.sogou.com/weixin?type=2&query={name}&page={page}' for page in
                       range(1, pages + 1)]
        xpath = '//*[@class="news-list"]/li'
        articles = []
        for search_url in search_urls:
            html_tree = self._get_html(search_url)
            article_nodes = html_tree.xpath(xpath)
            for article_node in article_nodes:
                article_url = article_node.xpath('./div[2]/h3/a/@href')[0]
                official_account_url = article_node.xpath('./div[2]/div/a/@href')[0]
                digest = article_node.xpath('./div[2]/p')[0].text_content()
                articles.append(Article(article_url, official_account_url, digest))
        return articles

    def search_official_account(self, wechat_id):
        search_url = f'http://weixin.sogou.com/weixin?type=1&query={wechat_id}'
        html_tree = self._get_html(search_url)
        xpath = '//*[@id="main"]/div[4]/ul/li[1]/div/div[2]'
        official_account = html_tree.xpath(xpath)
        if official_account:
            official_account = official_account[0]
            if wechat_id == official_account.xpath('./p[2]/label/text()')[0]:
                return OfficialAccount(official_account.xpath('./p[1]/a/@href')[0])
        return None

    def _get_html(self, url):
        resp = self._session.get(url)
        if url == resp.url:
            return html.document_fromstring(resp.text)
        else:
            cookies = utils.dict_from_cookiejar(self._session.cookies)
            snuid = self._identify_captcha()
            cookies['SNUID'] = snuid
            cookies['SUV'] = snuid
            self._session.cookies = utils.cookiejar_from_dict(cookies)
            return self._get_html(url)

    def _identify_captcha(self):
        while True:
            resp = self._session.get('http://weixin.sogou.com/antispider/util/seccode.php?tc=100000')
            tf = TemporaryFile()
            tf.write(resp.content)
            image = Image.open(tf)
            code = self._identify(image)
            resp = self._session.post('https://weixin.sogou.com/antispider/thank.php', data={
                'c': code,
                'r': 'https://weixin.sogou.com/',
                'v': 5
            })
            resp.encoding = 'utf-8'
            msg = resp.json()
            if msg['code'] == 0:
                return msg['id']
            print('验证码输入错误！')

    def _identify(self, image):
        image.show()
        return input('Sougo验证码：')
