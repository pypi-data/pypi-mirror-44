from sgwc import search_articles, setting

# setting.get_proxy = lambda: {
#         'http': 'http://119.102.26.186:9999',
#         'https': 'http://119.102.26.186:9999',
#     }

articles = search_articles('lol')
for article in articles:
    print(article)
