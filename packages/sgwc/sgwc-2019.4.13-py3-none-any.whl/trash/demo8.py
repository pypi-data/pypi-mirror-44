from requests import Session

session = Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 ',

}

host = '192.168.0.107'
port = '8888'
resp = session.get(
    url='http://weixin.sogou.com/weixin?type=2&query=lol&page=1',
    # url='https://weixin.sogou.com/',
    # url='https://icanhazip.com/',
    proxies={
        'http': f'http://{host}:{port}',
        'https': f'http://{host}:{port}',
    })
resp.encoding = 'utf-8'
print(resp.text)
