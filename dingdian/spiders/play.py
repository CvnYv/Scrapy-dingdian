import requests
from bs4 import BeautifulSoup
import re

headers = {'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                         ' (KHTML, likeGecko) Ubuntu Chromium/58.0.3029.81 C'
                         'hrome/58.0.3029.81 Safari/537.36'
           }
# html = requests.get('http://www.23us.com/book/64556', headers=headers).text
# name = BeautifulSoup(html, 'lxml').find('h1').get_text().split()[0]
# bs_table = BeautifulSoup(html, 'lxml').find('table')
# author = bs_table.find_all('td')[1].get_text().split()[0]
# novelurl = BeautifulSoup(html, 'lxml').find('a', class_='read')['href']
# status = bs_table.find_all('td')[2].get_text().split()[0]
# number = bs_table.find_all('td')[4].get_text().split()[0][:-1]
# category = bs_table.find_all('td')[0].get_text().split()[0]
# name_id = re.findall('down/(\d+)', html)[0]
url = 'http://www.23us.com/class/6_1.html'
html = requests.get('http://www.23us.com/class/6_1.html', headers=headers).text
pattern = '>1/(\d+)<'
max_num = re.findall(pattern, html)[0]  # 构建re获取各个类型的最大页面数
prefix_url = str(url)[0:28]
for num in range(1, int(max_num)+1):
    url = prefix_url + str(num) + '.html'
    print(url)