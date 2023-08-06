from requests import Session
from PIL import Image
from tempfile import TemporaryFile

session = Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 ',
    # 'Referer': 'https://weixin.sogou.com'
}
resp = session.get('https://weixin.sogou.com/antispider/util/seccode.php?tc=1555075719')
tf = TemporaryFile()
tf.write(resp.content)
Image.open(tf).show()
print(resp.content)