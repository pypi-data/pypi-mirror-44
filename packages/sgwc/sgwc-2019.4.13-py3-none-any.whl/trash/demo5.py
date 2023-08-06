import wechatsogou
# ws_api =wechatsogou.WechatSogouAPI()
ws_api = wechatsogou.WechatSogouAPI(proxies={
"http": "27.29.46.11:9999",
"https": "27.29.46.11:9999",
})
print(list(ws_api.search_article('lol')))