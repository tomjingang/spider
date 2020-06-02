from bs4 import BeautifulSoup
import time 
import random
import ssl
from urllib import request, parse, error
import re
import pandas as pd
import os


User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
headers = {'User-Agent': User_Agent}

url = 'https://www.outletcity.com/de/metzingen/marken-outlet/'

data = request.Request(url=url, headers=headers)
response = request.urlopen(data)
html = response.read().decode()
data = BeautifulSoup(html, 'html.parser')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

list_nametitle = [chr(i) for i in range(65,91)]
i = 0
marke_info ={}
marke = []

for p in range(0,26):

    try:
        marke_title = list_nametitle[p]
        marke_list = data.find('div', attrs ={'id':'brand'+ marke_title})
        marke_list_i = marke_list.find('ul')
        marke_categories = marke_list.find_all('li')
        marke_name_i = marke_list_i.find_all('a')
        
        for ii in marke_categories:
        
            #marke_list_i = marke_list.find('li')
            # print(marke_list_i)
            #marke_name = marke_list_i.getText().replace('', '')
            #print (marke_name)
            markename_nameurl = ii.find('a').get('href')
            markename_name = ii.find('a').getText().replace('\n', '').replace('\s','')

            marke_categorie = ii.get('data-categories').replace('womenFashion', '女士').replace('kidsFashion','儿童').replace('menFashion', '男士').replace('shoes', '鞋子').replace('sportAndOutdoor', '运动').replace('underwearAndLingerie','内衣').replace('bagsAndAccessoires','包和首饰').replace('watchesAndJewellery', '手表和珠宝').replace('category-', '   ').replace('cosmetics', '化妆品').replace(',', '')
            marke_categorie.rstrip()
            categorie_list = marke_categorie.split()
            for i in categorie_list:
                if '女士' in categorie_list:
                    womenFashion = '有售'
                else:
                    womenFashion = '不销售'
            
            for i in categorie_list:
                if '男士' in categorie_list:
                    menFashion = '有售'
                else:
                    menFashion = '不销售'

            for i in categorie_list:
                if '化妆品' in categorie_list:
                    cosmetics = '有售'
                else:
                    cosmetics = '不销售'
            for i in categorie_list:
                if '鞋子' in categorie_list:
                    shoes = '有售'
                else:
                    shoes = '不销售'
            for i in categorie_list:
                if '运动' in categorie_list:
                    sports = '有售'
                else:
                    sports = '不销售'
            for i in categorie_list:
                if '手表和珠宝' in categorie_list:
                    watches = '有售'
                else:
                    watches = '不销售'

            markename_name = re.sub(' +', '', markename_name)
            marke_info = {'Name':markename_name, 'Url':'www.outletcity.com'+ markename_nameurl,'女士':womenFashion, '男士':menFashion,
            '化妆品':cosmetics, '运动':sports, '鞋子':shoes, '手表和珠宝': watches}
            marke.append(marke_info)



        print('已完成' + str(p+1) + '/26')

    except:
        print('已完成' + str(p+1) + '/26')


print('已获取全部数据')



path = 'E:/place/outlets.xlsx'

try:
    if os.path.exists(path):
        df = pd.read_excel(path)
        df = df.append(marke)
    else:
        df = pd.DataFrame(marke)
except:
    print ('heihei')

writer = pd.ExcelWriter(path)

df.to_excel(excel_writer=writer, 
                columns = ['Name', '女士','男士','鞋子','化妆品','运动','手表和珠宝','Url'], index = False,
                encoding = 'utf-8', sheet_name='Marke in Outlets')
writer.save()
writer.close()

