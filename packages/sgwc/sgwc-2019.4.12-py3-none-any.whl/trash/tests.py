from sgwc import search_officials, search_articles, get_official


def test_get_official():
    official = get_official('LOL313298553')
    print(official)
    print(f"""
        url  ---  {official.url}
        official_id  ---  {official.official_id}
        name  ---  {official.name}
        avatar_url  ---  {official.avatar_url}
        qr_code_url  ---  {official.qr_code_url}
        profile_desc  ---  {official.profile_desc}
        recent_article  ---  {official.recent_article}
        articles  ---  {official.articles}
        authenticate  ---  {official.authenticate}
        monthly_articles  ---  {official.monthly_articles}
        monthly_visits  ---  {official.monthly_visits}
    """)


def test_search_articles():
    articles = search_articles('lol')
    print(articles)
    print(f"""
        url  ---  {articles[0].url}
        title  ---  {articles[0].title}
        date  ---  {articles[0].date}
        image_url  ---  {articles[0].image_url}
        digest  ---  {articles[0].digest}
        official_url  ---  {articles[0].official_url}
        official_name  ---  {articles[0].official_name}
        official  ---  {articles[0].official}
    """)
    print(articles[0].official.recent_article, type(articles[0].official.recent_article))


def test_search_officials():
    officials = search_officials('lol')
    print(officials)
    print(officials[0].articles)


def test_get_official_from_url():
    articles = search_articles('lol')
    official = articles[0].official
    print(official)
    print(f"""
        url  ---  {official.url}
        official_id  ---  {official.official_id}
        name  ---  {official.name}
        avatar_url  ---  {official.avatar_url}
        qr_code_url  ---  {official.qr_code_url}
        profile_desc  ---  {official.profile_desc}
        recent_article  ---  {official.recent_article}
        articles  ---  {official.articles}
        authenticate  ---  {official.authenticate}
        monthly_articles  ---  {official.monthly_articles}
        monthly_visits  ---  {official.monthly_visits}
    """)


def test_article_save():
    articles = search_articles('lol')
    for article in articles:
        article.save('markdown')


if __name__ == '__main__':
    # test_get_official()
    # test_search_articles()
    # test_search_officials()
    # test_get_official_from_url()
    test_article_save()
