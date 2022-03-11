from lxml import etree
import requests
import json


url = 'https://news.sina.com.cn/'
resp = requests.get(url=url)
resp.encoding = resp.apparent_encoding

tree = etree.HTML(resp.text)
news_ls = tree.xpath('//*[@id="ad_entry_b2"]/ul/li/a')
news_dict = {}
for a in news_ls:
    print('%s: %s' % (a.text, a.attrib.get('href')))
    news_dict[a.text] = a.attrib.get('href')
