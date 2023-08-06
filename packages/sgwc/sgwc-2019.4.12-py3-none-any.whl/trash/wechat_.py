from lxml.html import document_fromstring, tostring
from tempfile import TemporaryFile
from requests import Session
# from .attributes import *
from PIL import Image

_session = Session()


class Article:
    # todo: How create const
    _INFO_LIST = ()
    _DETAIL_INFO_LIST = ()

    def __init__(self, **params):
        assert 'url' in params  # todo: Something prompt
        self._info = params
        self._is_detail = False

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __getattr__(self, key):
        pass

    def __setattr__(self, key, value):
        pass

    @property
    def info(self, is_detail=False):
        return self._info

    @property
    def official(self):
        return None

    def save(self):
        pass

    def get_detail(self):
        pass


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
