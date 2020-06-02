from bs4 import BeautifulSoup
import time 
import random
import ssl
from urllib import request, parse, error
import re

url = 'http://www.chinamoney.com.cn/chinese/qwjsn/?searchValue=%25E5%25AE%2589%25E5%2590%2589%25E5%258E%25BF%25E5%259F%258E%25E5%25B8%2582%25E5%25BB%25BA%25E8%25AE%25BE%25E6%258A%2595%25E8%25B5%2584%25E9%259B%2586%25E5%259B%25A2%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
headers = {'User-Agent': User_Agent}


from requests_html import HTMLSession

session = HTMLSession()
r = session.get(url=url, headers=headers)
r.html.render(scrolldown=50,sleep=0.2)
list =  r.html.find('.san-grid-f-m')[1].find('a')[0].attrs['onclick'].split(',')[7][1:-3]
print(list)
# 获取首页新闻标签、图片、标题、发布时间
# for x in r.html.find('.packery-item'):
#     yield {
#         'tag': x.find('.category')[0].text,
#         'image': x.find('.lazyload')[0].attrs['data-src'],
#         'title': x.find('.smart-dotdotdot')[0].text if x.find('.smart-dotdotdot') else x.find('.smart-lines')[0].text,
#         'addtime': x.find('.smart-date')[0].attrs['data-origindate'][:-6]
#     }







# for i in range(len(otherUrl)):
#     folder = '%d.'%(i+1) + company_name[i]
#     if (os.path.exists(folder) == False):
#         os.mkdir(folder)
#         os.chdir(folder)
#     req = Request(url)
#     req.add_header("User-Agent",
#                    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36")
#     res = urlopen(req)
#     data = res.read().decode("utf-8")
#     # 使用beautifulsoup
#     soup = BeautifulSoup(data, "lxml")
#
#     # 包含tr的对象列表
#     infoList = soup.find_all('tr')

