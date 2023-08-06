from time import strftime, localtime
from lxml.html import tostring
from re import findall
from json import loads

__all__ = ['official_id_', 'official_name_', 'official_avatar_url_', 'official_qr_code_url_', 'official_profile_desc_',
           'official_authenticate_', 'official_articles_']


def official_id_(html_tree):
    return html_tree.xpath('/html/body/div/div[1]/div[1]/div[1]/div/p/text()')[0][5:]


def official_name_(html_tree):
    return html_tree.xpath('/html/body/div/div[1]/div[1]/div[1]/div/strong/text()')[0].strip()


def official_avatar_url_(html_tree):
    return html_tree.xpath('/html/body/div/div[1]/div[1]/div[1]/span/img/@src')[0]


def official_qr_code_url_(html_tree):
    return html_tree.xpath('//*[@id="js_pc_qr_code_img"]/@src')[0]


def official_profile_desc_(html_tree):
    profile_desc = html_tree.xpath('/html/body/div/div[1]/div[1]/ul/li[1]/div/text()')
    return profile_desc[0] if profile_desc else None


def official_authenticate_(html_tree):
    authenticate = html_tree.xpath('/html/body/div/div[1]/div[1]/ul/li[2]/div/text()')
    return authenticate[0] if authenticate else None


def official_articles_(html_tree):
    html_text = tostring(doc=html_tree, encoding='unicode')
    domain_name = 'http://mp.weixin.qq.com'
    result = findall('var msgList = {"list":(\[.*?\])};', html_text)
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
                'date': date,
                'digest': article_item['digest'],
                'image_url': article_item['cover'],
            })
    return article_items
