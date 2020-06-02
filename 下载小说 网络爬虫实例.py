# https://www.biqukan.com/1_1094/
from urllib import request
from bs4 import BeautifulSoup
import socket
import requests
import re
import threading
import time



def get_next_page_url(url):

    net_status = False
    while not net_status:

        try:

            a_list = []
            a_list1 = []
            a_list2 = []

            response = request.urlopen(url=url, timeout =5)

            # html = response.read().decode()

            html = response.read().decode('gbk')

            html_soup = BeautifulSoup(html, 'html.parser')

            a_list1 = html_soup.find('div',attrs={'class':'page_chapter'})
            a_list2 = a_list1.find('ul')
            a_list = a_list2.find_all('li')[2].find('a').get('href')
            
            

            target_url = str('https://www.biqukan.com' + a_list)
            
            
            return target_url
        except socket.timeout:
            print ('connect failure')
            net_status = False



def get_all_page_url(url,tlc):

    chapters_list = []

    urls_list = []

    net_status = False

    

    while not net_status:

        try:

            response = request.urlopen(url=url, timeout=5)

            html = response.read().decode('gbk')

            html_soup = BeautifulSoup(html, 'html.parser')

            

            a_list1 = html_soup.find('div', attrs={'class' : 'listmain'})
            a_list2 = a_list1.find('dl')
            dd_list = a_list2.find_all('dd')
            
            
            for i in dd_list[tlc:tlc+300]:

                chapters_list.append(i.getText())

                i = str(i.find('a').get('href'))
                this_url = 'https://www.biqukan.com' + i
                next_url = get_next_page_url(this_url)

                
    
                #urls_list.append(this_url)
                
                urls_list.append(next_url)

                
            
            


            return chapters_list, urls_list

            # for i in dd_list[13:]:

                # if '.html' in str(i):

                # i_soup = BeautifulSoup(str(i), 'html.parser')

                    
                # this_url = 'https://www.biqukan.com' + str(i.find('a').get('href'))
                # next_url = get_next_page_url(this_url)
                # chapters_list.append(str(i_soup.getText())
                # urls_list.append(this_url)
                # urls_list.append(next_url)

        #     return chapters_list, urls_list
        except socket.timeout:
            print('Connect failure')
            net_status = False


def parse_page(url):

    net_status = False

    while not net_status:

        try:

            response = request.urlopen (url=url, timeout=5)

            html = response.read().decode('gbk')

            html_soup = BeautifulSoup(html, 'html.parser')

            current_text1 = html_soup('div', attrs={'class':'showtxt'})

            for i in current_text1:


                current_text = str(i.getText()).replace('<br/>', '\r\r' )

            if '请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：wap.biqukan.com' in current_text:
                current_text = current_text.replace('请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：wap.biqukan.com', '')
                current_text = current_text.replace('('+url+')' , '')
                current_text = current_text.replace('chaptererror();' , '')

            return current_text

        except socket.timeout:
            print('Connect failure')
            net_status = False



        
def download(tlc) :       

    url = 'https://www.biqukan.com/1_1094'

    chapters, urls = get_all_page_url(url, tlc)

    for ul in urls:

        ul_index = urls.index(ul)

        title = chapters[ul_index]

        cu_text = parse_page(ul)

        savepath = 'E:/一念永恒' + '\\' + str(title) + '.txt'              # 新建文件命名方法

        with open (savepath, 'a', encoding = 'utf-8') as f_obj:

            f_obj.write(str(title) + '\n')
            f_obj.write(str(cu_text) +'\n\n')
        
        


def test1(arg1):
    print("启动任务1")
    download(13)
    time.sleep(6)
    print("结束任务1")


def test2(arg2):
    print("启动任务2")
    download(314)
    time.sleep(2)
    print("结束任务2")


def test3(arg3):
    print("启动任务3")
    download(615)
    time.sleep(5)
    print("结束任务3")


def main():
    start_time = time.ctime()
    print("启动主任务：{}".format(start_time))
    t1 = threading.Thread(target=test1,args=("ONE",))
    # setName 给子线程命名
    t1.setName("TH-1")
    t1.start()


    t2 = threading.Thread(target=test2,args=("TWO",))
    t2.setName("TH-2")
    t2.start()


    t3 = threading.Thread(target=test3,args=("THREE",))
    t3.setName("TH-3")
    t3.start()
    # 睡眠3秒，任务2结束
    time.sleep(3)
    # enumerate 得到正在运行的进程
    for i in threading.enumerate():
        # getName 获取线程名
        name = i.getName()
        print("正在运行的进程有：{}".format(name))
    # 获取正在运行的进程数量
    num = threading.activeCount()
    print("正在运行的进程数量有{}个".format(num))
    print("结束主任务")

if __name__ == '__main__':
    
    main()


    