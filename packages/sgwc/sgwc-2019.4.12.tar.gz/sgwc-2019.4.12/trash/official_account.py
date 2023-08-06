from time import localtime, strftime
from tempfile import TemporaryFile
from .article import Article
from requests import Session
from re import findall
from json import loads
from lxml import html
from PIL import Image


class OfficialAccount:
    def __init__(self, url):
        self._url = url
        self._session = Session()
        self._html_tree = self._get_html(url)
        self._name = self._get_name()
        self._wechat_id = self._get_wechat_id()
        self._profile_desc = self._get_profile_desc()
        self._account_body = self._get_account_body()
        self._article_items = self._get_article_items()
        self.article_num = len(self._article_items)
        self._articles = self._get_articles()

    def _get_name(self):
        xpath = '/html/body/div/div[1]/div[1]/div[1]/div/strong/text()'
        return self._html_tree.xpath(xpath)[0].strip()

    def _get_wechat_id(self):
        xpath = '/html/body/div/div[1]/div[1]/div[1]/div/p/text()'
        return self._html_tree.xpath(xpath)[0][5:]

    def _get_profile_desc(self):
        xpath = '/html/body/div/div[1]/div[1]/ul/li[1]/div/text()'
        profile_desc = self._html_tree.xpath(xpath)
        return profile_desc[0] if profile_desc else None

    def _get_account_body(self):
        xpath = '/html/body/div/div[1]/div[1]/ul/li[2]/div/text()'
        account_body = self._html_tree.xpath(xpath)
        return account_body[0] if account_body else None

    def _get_article_items(self):
        html_text = html.tostring(self._html_tree, method="html", encoding='utf-8')
        domain_name = 'http://mp.weixin.qq.com'
        result = findall(b'var msgList = {"list":(\[.*?\])};', html_text)
        if not result:
            return []
        article_items = []
        for item in loads(result[0]):
            date = strftime('%Y-%m-%d', localtime(item['comm_msg_info']['datetime']))
            for article_item in item['app_msg_ext_info']['multi_app_msg_item_list']:
                url = article_item['content_url'] if article_item['content_url'].startswith('http') \
                    else domain_name + article_item['content_url']
                article_items.append({
                    'url': url.replace('&amp;', '&'),
                    'title': article_item['title'],
                    'author': article_item['author'],
                    'digest': article_item['digest'],
                    'date': date,
                })
        return article_items

    def _get_articles(self):
        return [Article(item['url'], self, item['digest']) for item in self._article_items]

    @property
    def url(self):
        return self._url

    @property
    def name(self):
        return self._name

    @property
    def wechat_id(self):
        return self._wechat_id

    @property
    def profile_desc(self):
        return self._profile_desc

    @property
    def account_body(self):
        return self._account_body

    @property
    def article_urls(self):
        return [item['url'] for item in self._article_items]

    @property
    def articles(self):
        return self._articles

    @property
    def article_items(self):
        return self._article_items

    def _get_html(self, url):
        resp = self._session.get(url)
        if '请输入验证码' in resp.text:
            self._identify_captcha()
            return self._get_html(url)
        else:
            return html.document_fromstring(resp.text)

    def _identify_captcha(self):
        while True:
            resp = self._session.get('http://mp.weixin.qq.com/mp/verifycode?cert=100000')
            tf = TemporaryFile()
            tf.write(resp.content)
            image = Image.open(tf)
            code = self._identify(image)
            resp = self._session.post('http://mp.weixin.qq.com/mp/verifycode',
                                      data=f'cert={100000}&input={code}&appmsg_token=""')
            resp.encoding = 'utf-8'
            msg = resp.json()
            if msg['ret'] == 0:
                break
            print('验证码输入错误！')

    def _identify(self, image):
        image.show()
        return input('Weixin验证码：')
