# 本代码用来爬取aa.achives.gov.tw下，存在于对应文件中每个案的所有图片
# 使用到了selenium模拟自动化操作 base64解码 os创建文件夹 src码的知识
import time
import re
import pandas as pd 
from selenium import webdriver
import base64
import os
import multiprocessing
import shutil



def mkdir(path):# makedirs 创建文件时如果路径不存在会创建这个路径
        
    folder = os.path.exists(path)

    if not folder:                   # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
        status = False           
    else:
        status = True            
    return status                  # 若已经存在文件夹，返回False的status

def get_url_list(xls): # 从excel文件中提取相应列，并与基础域名合并，成为每个 案 所对应的网站的url
    url_list = [] 
    for i in xls['檔號']:

        url = 'https://aa.archives.gov.tw/ELK/SearchImageDetailed?fullpath=' + i
    
        name =xls[(xls['檔號']==i)]['案由']
        id = i.replace('/', '=')
        for na in name: 
            an_name = na.replace('/', '=').replace(':','=')
            file_name =  "F:\图片_案/" + an_name + '_' + str(id)
            # img_name_title = na
            status = mkdir(file_name)       # 创建以 案的名字 为名字的文件夹. 
            # 注意 如果案的名字中出现 / 会默认为下一层目录，所以需要替换


        url_list.append(url) 
    return url_list,status         # 返回每个案所对应的url列表

def img_fuc(url,status,xls): # 下载图片

    # 通过使用selenium，模拟人打开页面，从而获得js动态加载的图片的信息。
    # print('3')
    fail_an = []
    fail_img = []
    if status:
        return   # 如果已经存在对应的文件夹，则不进行本函数下载图片的请求。因为已经下载过了

    # selemnium的基本代码如下
    i = url

    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式,建议先有界面情况调试，之后在使用无头模式，减少时间以及缓存
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    try:
        driver = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options) 
        driver.get(i)

        url_1 = driver.find_element_by_xpath('//input[@class="hFullPath"]').get_attribute('value')
    # 获得每个 案 的特征域名，其实这里与源数据中的档号相同。傻逼了

        nur = driver.find_element_by_xpath('//span[@class="pagination-info"]').text
        nr = int(re.findall('.*共(.*?)筆.*',nur)[0])
        # 获取每个 案 下面的所有图片数目


        name = xls[(xls['檔號']==i.replace('https://aa.archives.gov.tw/ELK/SearchImageDetailed?fullpath=',''))]['案由']
        id = i.replace('https://aa.archives.gov.tw/ELK/SearchImageDetailed?fullpath=','').replace('/','=')
        for na in name: 
            an_name = na.replace('/', '=').replace(':','=')

            file_name =  "F:\图片_案/" + an_name + '_' + str(id)
            img_name_title = na
        # 获取每个 案 的名字，方便在对应文件夹下载图片
        # 注意 如果案的名字中出现 / 会默认为下一层目录，所以需要替换


        # 开始下载图片。
        # src是图片在网络上的绝对路径。
        # 每个图片的src码是base64编码，所以要base64解码之后保存成图片格式
        # 每个案的每一页url相同，使用了js动态编码。两种方法，一种是通过表单找到每个图片的请求url，一种是使用selenium模拟人点击下一页。
        # 这里使用的是找到每个url的请求url
        n = 1

        print (img_name_title + '开始下载')
        while n <= nr:
            try:            
                url = 'https://aa.archives.gov.tw/ELK/LoadImages?encPath=' + url_1 + '&page='+ str(n)
                # 每张图片的请求url的格式

                driver.get(url)
                # 每张图片的base64码存在于，请求url对应的网页中6

                img_src = driver.find_element_by_xpath('//body').text.replace('data:image/png;base64,','')
                # 网页显示base64的图片时，需要加上前缀。去掉前缀之后，便是电脑的base64所需要的解码素材

                img_name = file_name + '/'+ img_name_title + '_' + str(n) + '.jpg'
                
                # 使用base64解码储存图片
                with open(img_name,'wb') as file: # 如果不存在img_name这个文件，则自动创建

                    img = base64.b64decode(img_src)

                    file.write(img)

            except:
                fail_img = [img_name_title,]
                fail_img.append(n)
                print(img_name_title + '中的' + '-' + str(n) + '下载失败')

            n += 1
        
        driver.close()
    except:
        
        name = xls[(xls['檔號']==url.replace('https://aa.archives.gov.tw/ELK/SearchImageDetailed?fullpath=',''))]['案由']
        id = url.replace('https://aa.archives.gov.tw/ELK/SearchImageDetailed?fullpath=','').replace('/','=')
        for na in name: 
            print(na + '下载失败')
            an_name = na.replace('/', '=')
            file_name =  "F:\图片_案/" + an_name + '_' + str(id)
            fail_an.append(an_name +  '_' + str(id))
            shutil.rmtree(file_name)

    return fail_an,fail_img
   


def multi_process(url_list,status,xls): # 多线程爬虫
    pool = multiprocessing.Pool(processes=4) # 使用cpu可用的线程数，同时进行爬虫

    fail_an = []
    fail_an_list = []
    for url in url_list:

        
        # fail_an = p.get()

        fail_an.append(pool.apply_async(img_fuc, (url,status,xls)))
        time.sleep(2)
            # fail_img_list.append(fail_download)
        # 第一个为函数，第二个为对应参数
    for an in fail_an:
        an_get = an.get()
        if an_get != ([],[]):
            fail_an_list.append(an_get)
    pool.close()
    pool.join()
    return fail_an_list
    

if __name__ == "__main__":



    document = input('请输入想要下载图片的文件名：')
    xls = pd.read_excel(document )
    url_list,status = get_url_list(xls)
    fail_an_list = multi_process(url_list,status,xls)
    

    print('下载失败：', fail_an_list)



