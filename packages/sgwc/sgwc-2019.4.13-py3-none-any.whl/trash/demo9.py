from sgwc import search_articles

articles = search_articles('lol')
for a in articles:
    print(a)
    print(a.items())
