from bs4 import BeautifulSoup
import time 
import random
import ssl
from urllib import request, parse, error
import re



def get_data(url):
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    headers = {'User-Agent': User_Agent}

    data = request.Request(url=url, headers=headers)
    response = request.urlopen(data)
    html = response.read().decode()
    data = BeautifulSoup(html, 'html.parser')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

   

    return data


def get_url(url,p):
    url_list = []
    data_soup = get_data(url)
    

    for i in range (p, p+9):
    

        list_1 = data_soup.find('div', attrs={'class':'result', 'id': str(i)})
        if list_1 != None:
            list_2 = list_1.find('h3').find('a').get('href')
            print(list_2)

        else: 
            print ('id' + str(i) + '对应的url不存在')
        # time.sleep(random.randint(2,5))



        url_item = data_soup.find('div', attrs={'id' : 'page'})
        url_i = url_item.find_all('a')
        for aa in url_i:
            url_page = aa.get('href').replace('/s?', '')
            url_list.append(url_page)

    return url_list, list_2

def irterativ(url):

    
    get = get_url(url,1)
    url_list = get[0]
    list_2 = get[1]
    num = 1
    page = 1
    for i in url_list:
        url_new = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=64075107_1_dg&' + str (i)
        print ('已经打印到第' + str(page) + '页')
        page = page + 1
        num = num + 10
        
        new_get = get_url(url_new,num)
        time.sleep(random.randint(2,5))

        if new_get == None:
            print ('finish')


def main():
    url = input ('请输入初始网址:')
    irterativ(url)
    # get_url(url)

main()




        

        
