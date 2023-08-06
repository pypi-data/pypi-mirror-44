from requests import Session
from lxml import html
from re import search


class Article:

    def __init__(self, url, official_account, digest=None):
        self._url = url
        self._session = Session()
        self._html_tree = self._get_html(url)
        self._title = self._get_title()
        self._official_account = official_account
        self._date = self._get_date()
        self._digest = digest

    def _get_html(self, url):
        return html.document_fromstring(self._session.get(url).text)

    def _get_title(self):
        xpath = '//*[@id="activity-name"]/text()'
        return self._html_tree.xpath(xpath)[0].strip()

    def _get_date(self):
        html_text = html.tostring(self._html_tree)
        return search('var publish_time = "(.*?)" \|\| "";', str(html_text))[1].strip()

    def _get_content(self):
        xpath = '//*[@id="js_content"]'
        return self._html_tree.xpath(xpath)[0]

    def save(self, directory_path):
        with open(f'{directory_path}/{self._title}.md', 'wb') as file:
            content_node = self._get_content()
            contents = [html.tostring(node) for node in content_node]
            text = b'\n'.join(contents)
            text = text.replace(b' data-', b' ')
            file.write(text)

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
    def official_account(self):
        return self._official_account

    @property
    def digest(self):
        return self._digest
