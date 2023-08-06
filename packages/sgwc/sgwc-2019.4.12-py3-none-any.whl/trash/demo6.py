from requests import Session
from requests.utils import add_dict_to_cookiejar
session = Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 ',
    'Referer': 'https://weixin.sogou.com/weixin?type=2&page=1&ie=utf8&query=lol&interation=',
}

print(session.cookies)
resp = session.get('http://www.baidu.com')
resp.encoding = 'utf-8'
print(session.cookies)
add_dict_to_cookiejar(session.cookies, {'name': 'czw'})
print(session.cookies)
session.headers.update({'name': 'czw'})
print(session.headers)
print(resp.cookies)
