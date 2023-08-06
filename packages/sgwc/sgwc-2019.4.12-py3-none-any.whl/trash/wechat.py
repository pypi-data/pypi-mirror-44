from lxml.html import document_fromstring, tostring
from tempfile import TemporaryFile
from requests import Session
from trash.attributes import *
from PIL import Image

_session = Session()


class Article:
    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)

    def __init__(self, url, title, date, official_url, official_name, digest='', image_url=None):
        self._url = url
        self._title = title
        self._date = date
        self._image_url = image_url
        self._digest = digest
        self._official_url = official_url
        self._official_name = official_name
        self._official = None
        self._html_tree = None

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self._date

    @property
    def image_url(self):
        return self._image_url

    @property
    def digest(self):
        return self._digest

    @property
    def official_url(self):
        return self._official_url

    @property
    def official_name(self):
        return self._official_name

    @property
    def official(self):
        return self._official if self._official else Official.from_url(self._official_url)

    @property
    def info(self):
        return {
            'url': self._url,
            'title': self._title,
            'date': self._date,
            'digest': self._digest,
            'official_url': self._official_url,
            'official_name': self._official_name,
        }

    def save(self, path='.'):
        if not self._html_tree:
            self._html_tree = document_fromstring(_get_html(self._url))
        title = self._title
        title = title.replace('/', '-').replace('\\', '-').replace(':', '：').replace('*', '-')
        title = title.replace('"', '”').replace('|', '-').replace('<', '-').replace('>', '-').replace('?', '？')
        with open(f'{path}/{title}.md', 'w', encoding='utf-8') as file:
            content_node = self._html_tree.xpath('//*[@id="js_content"]')[0]
            contents = [tostring(node, encoding='unicode') for node in content_node]
            text = '\n'.join(contents)
            text = text.replace(' data-', ' ')
            file.write(text)


class Official:
    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)

    def __init__(self, url, official_id, name, avatar_url, qr_code_url, profile_desc, status=(), recent_article=None):
        self._url = url
        self._official_id = official_id
        self._name = name
        self._avatar_url = avatar_url
        self._qr_code_url = qr_code_url
        self._profile_desc = profile_desc
        self._status = status
        self._recent_article = recent_article
        self._articles = []
        self._authenticate = None
        self._html_tree = None

    @property
    def url(self):
        return self._url

    @property
    def official_id(self):
        return self._official_id

    @property
    def name(self):
        return self._name

    @property
    def avatar_url(self):
        return self._avatar_url

    @property
    def qr_code_url(self):
        return self._qr_code_url

    @property
    def profile_desc(self):
        return self._profile_desc

    @property
    def recent_article(self):
        if not self._recent_article:
            self._get_html()
            articles = []
            for article_item in official_articles_(self._html_tree):
                article = Article(**article_item, official_url=self._url, official_name=self._name)
                article._official = self
                articles.append(article)
            self._articles = articles
            self._recent_article = self._articles[0] if self._articles else None
        return self._recent_article

    @property
    def articles(self):
        if not self._articles:
            self._get_html()
            articles = []
            for article_item in official_articles_(self._html_tree):
                article = Article(**article_item, official_url=self._url, official_name=self._name)
                article._official = self
                articles.append(article)
            self._articles = articles
            self._recent_article = self._articles[0] if self._articles else None
        return self._articles

    @property
    def authenticate(self):
        if not self._authenticate:
            self._get_html()
            self._authenticate = official_authenticate_(self._html_tree)
        return self._authenticate

    @property
    def monthly_articles(self):
        return self._status[0] if self._status else None

    @property
    def monthly_visits(self):
        return self._status[1] if self._status else None

    @property
    def info(self):
        return {
            'url': self._url,
            'official_id': self._official_id,
            'name': self._name,
            'profile_desc': self._profile_desc,
            'status': f'月发文 {self._status[0]}篇，月访问 {self._status[1]}次' if self._status else None,
            'recent_article': self._recent_article,
        }

    @classmethod
    def from_url(cls, url):
        html_tree = document_fromstring(_get_html(url))
        official_id = official_id_(html_tree)
        official_name = official_name_(html_tree)
        official_avatar_url = official_avatar_url_(html_tree)
        official_qr_code_url = official_qr_code_url_(html_tree)
        official_profile_desc = official_profile_desc_(html_tree)
        official_authenticate = official_authenticate_(html_tree)
        official_articles = official_articles_(html_tree)
        official = cls(url, official_id, official_name, official_avatar_url, official_qr_code_url,
                       official_profile_desc)
        for article_item in official_articles:
            article = Article(**article_item, official_url=url, official_name=official_name)
            article._official = official
            official._articles.append(article)
        official._authenticate = official_authenticate
        official._recent_article = official._articles[0]
        official._html_tree = html_tree
        return official

    def _get_html(self):
        if self._html_tree is None:
            self._html_tree = document_fromstring(_get_html(self._url))


def _get_html(url):
    resp = _session.get(url)
    if '请输入验证码' in resp.text:
        _identify_captcha()
        return _get_html(url)
    else:
        return resp.text


def _identify_captcha():
    while True:
        resp = _session.get('http://mp.weixin.qq.com/mp/verifycode?cert=100000')
        tf = TemporaryFile()
        tf.write(resp.content)
        captcha_image = Image.open(tf)
        code = _identifying(captcha_image)
        resp = _session.post('http://mp.weixin.qq.com/mp/verifycode',
                             data=f'cert={100000}&input={code}&appmsg_token=""')
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['ret'] == 0:
            break
        print('验证码输入错误！')


def _identifying(captcha_image):
    captcha_image.show()
    return input('WeChat验证码：')
