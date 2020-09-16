import webbrowser
import time


def url_open(url):
    webbrowser.open(url)
    time.sleep(0.1)


# アメダス
url_open('https://tenki.jp/amedas/3/11/')
# 予報
url_open('https://tenki.jp/forecast/3/11/4020/8217/1hour.html')
# 気象衛星画像
url_open('https://tenki.jp/satellite/japan-east/')
# POTEKA NET
url_open('http://www.potekanet.com/')
# GPV
url_open('http://weather-gpv.info/')
# SCW
url_open('https://supercweather.com/')
# 時系列予報
url_open(
    'https://www.data.jma.go.jp/fcd/yoho/wdist/jp/#zoom:6/lat:34.822823/lon:136.318359/colordepth:normal/elements:wm')
# 高解像度降水ナウキャスト
url_open('https://www.jma.go.jp/jp/highresorad/')
# 降水短時間予報
url_open('https://www.jma.go.jp/jp/kaikotan/')
# 台風情報
url_open('https://www.jma.go.jp/jp/typh/')
# 日立市の気象予報
url_open('https://www.jsdi.or.jp/~hctenso/index.htm')
