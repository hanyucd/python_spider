# -*- coding: UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
QQ�Ķ����棬��ȡÿ����ҳÿ��С˵������
start_URL = http://dushu.qq.com/store/index/sortkey/1/ps/30/p/1

"""
class QqRead:
    # ��ʼ���� �������ַ �� ����
    def __init__(self, base_url):
        self.base_url = base_url

    ''' ����ҳ�룬 ��ȡ��ҳ����ȡ��URL '''
    def getPage(self, pageNum):
        # ÿ��ҳ������URL
        spider_url = self.base_url + str(pageNum)
        print '������ȡ����ҳURL��ַ:', spider_url
        # ��ȡ��ҳ
        request = requests.get(spider_url)
        # ��ȡ��ҳ���ݸ��ڱ���
        html = request.text
        # ��ȡ BeautifulSoup����
        soup = BeautifulSoup(html, 'html.parser')
        # �洢ÿҳ����Ҫ��ȡ�����ӣ���ʼ�����б�
        links = []
        # cssѡ������ͨ����ϲ���
        for link in soup.select('div .bookImgBox'):
            # ���ҳ�� ÿ��С˵URL
             only_url = link.a.get('href')
             links.append(only_url)
        length = len(links)
        print '��ҳ�湲����ȡ', length, '��URL.'
        # ����Ԫ��
        return links, length

    ''' �õ� page ����ȡ��URL; ��������ÿ��С˵������ page '''
    def details(self, pageNum):
        page_links, length = self.getPage(pageNum)
        for link in page_links:
            # С˵���� �����ֵ�
            datas = {}
            # ��ȡ��ҳ
            request = requests.get(link)
            # ��ȡ��ҳ���ݸ�ֵ�ڱ���
            html = request.text
            # ���� BeautifulSoup����
            soup = BeautifulSoup(html, 'html.parser')
            # cssѡ������ͨ����ϲ���; ѡ��Ҫ��ȡ������ | ���� list
            node = soup.select('div .book_info')[0]

            first_line_node =  node.find_all('dl')[0] # С˵��һ����Ϣ
            second_line_node = node.find_all('dl')[1] # С˵�ڶ�����Ϣ
            three_line_node = node.find_all('div')[1] # С˵��������Ϣ
            # С˵����
            datas['data'] = {
                'title': node.h3.a.string, # ����
                'grade': node.find_all('div')[0].span.b.font.string, #����
                'author': first_line_node.find_all('dd')[0].a.string, # ����
                'type': first_line_node.find_all('dd')[1].a.string, #����
                'word_number': first_line_node.find_all('dd')[2].string, #����
                'publish': second_line_node.find_all('dd')[0].string, # ������
                'popularity': second_line_node.find_all('dd')[1].string, # ����
                'price': second_line_node.find_all('dd')[2].string, # �۸�
                'collect': three_line_node.find_all('a')[1].find_all('span')[2].string, # �ղ���
                'recommend': three_line_node.find_all('a')[2].span.string, # �Ƽ���
                'praise': three_line_node.find_all('a')[3].span.string # ������
            }
            # С˵ URL
            datas['spider_url'] = link
            datas['current_page_length'] = length
            # �� python �������� JSON ��ʽ, ����4��
            data_json = json.dumps(datas, encoding = "UTF-8", ensure_ascii = False, indent = 4)
            print data_json

if __name__ == '__main__':
    base_url = 'http://dushu.qq.com/store/index/sortkey/1/ps/30/p/'
    qq_read = QqRead(base_url)
    # ����ȡ�� 1 - 10, ��ȡ 1 - 10 ҳ
    for i in range(1, 11):
        qq_read.details(i)

        # ������ȡ����ҳURL��ַ: http://dushu.qq.com/store/index/sortkey/1/ps/30/p/1
        # ��ҳ�湲����ȡ 30 ��URL.
        # {
        #     "spider_url": "http://dushu.qq.com/intro.html?bid=310949",
        #     "data": {
        #         "popularity": "3003",
        #         "grade": "3.6",
        #         "price": "VIP���",
        #         "word_number": "25����",
        #         "title": "�ֱ����������",
        #         "author": "������",
        #         "publish": "�й���ѧ�Ļ�����������޹�˾",
        #         "collect": "3003",
        #         "praise": "0",
        #         "recommend": "31",
        #         "type": "�й��ŵ�С˵"
        #     },
        #     "current_page_length": 30
        # }
        # {
        #     "spider_url": "http://dushu.qq.com/intro.html?bid=320438",
        #     "data": {
        #         "popularity": "52255",
        #         "grade": "4.2",
        #         "price": "5.99Ԫ",
        #         "word_number": "19����",
        #         "title": "����ܲ��3",
        #         "author": "������",
        #         "publish": "�й����ȳ�����",
        #         "collect": "52255",
        #         "praise": "6",
        #         "recommend": "674",
        #         "type": "���"
        #     },
        #     "current_page_length": 30
        # }
        # ......
