#! usr/bin/env python3
# -*- coding:utf-8 -*-


import scrapy
import re
from dingdian.items import DingdianItem
from scrapy.http import Request
from bs4 import BeautifulSoup


class DingdianSpider(scrapy.Spider):

    name = 'dingdian'  # 项目名称,必须是唯一的
    allowed_domains = ['23us.com']  # 域名
    start_urls = []  # 构建各个类型首页url的列表
    for i in range(1, 11):
        url = 'http://www.23us.com/class/%d_1.html' % i
        start_urls.append(url)

    def parse(self, response):
        '''
        解析每一个类型的首页url并返回这个类型的所有页面url
        :param response: 
        :return: 
        '''
        pattern = '>1/(\d+)<'
        html = response.text
        max_num = re.findall(pattern, html)[0]  # 构建re获取各个类型的最大页面数
        prefix_url = str(response.url)[0:28]
        for num in range(1, int(max_num)+1):
            url = prefix_url + str(num) + '.html'  # 构建每一页的完整url
            yield Request(url, callback=self.get_url)
            # 将页面的response交给get_url()函数处理

    def get_url(self, response):
        '''
        根据每个页面的url找到这个页面中所有书籍的简介url
        :param response: 
        :return: 
        '''
        # pattern1 = 'title="(.*?)简介"'  # name的正则表达式(偷懒用re)
        pattern2 = 'a href="(.*?)" title='  # 构造简介的url的正则表达式
        html = response.text
        # names = re.findall(pattern1, html)
        urls = re.findall(pattern2, html)
        for u in urls:
            yield Request(u, callback=self.get_all)  # 将简介的url交给get_all处理

    def get_all(self, response):
        '''
        处理页面,匹配各项内容并返回item字典
        :param response: 
        :return: 
        '''
        item = DingdianItem()
        html = response.text
        name = BeautifulSoup(html, 'lxml').find('h1').get_text().split()[0]
        novelurl = BeautifulSoup(html, 'lxml').find('a', class_='read')['href']
        bs_table = BeautifulSoup(html, 'lxml').find('table')
        author = bs_table.find_all('td')[1].get_text().split()[0]
        status = bs_table.find_all('td')[2].get_text().split()[0]
        number = bs_table.find_all('td')[4].get_text().split()[0][:-1]
        category = bs_table.find_all('td')[0].get_text().split()[0]
        name_id = re.findall('down/(\d+)', html)[0]
        item['name'] = name
        item['author'] = author
        item['novelurl'] = novelurl
        item['status'] = status
        item['number'] = number
        item['category'] = category
        item['name_id'] = name_id
        return item