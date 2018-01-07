import requests
from lxml import etree
import urllib

def get_frist(list):
    try:
        return list[0]
    except Exception as e:
        return ""
class CrawlUrl(object):
    """
    爬取所有详情页面的连接
    """
    def __init__(self,url,startpage,endpage):
        self.starturl = url
        self.urlset = set()
        self.startpage = int(startpage)
        self.endpage = int(endpage)
        self.content_dict = {}

    def crawl_url(self):
        for i in range(self.startpage,self.endpage):
            url = urllib.parse.urljoin(self.starturl,'?p={0}'.format(i))
            print(url)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
            }
            response = requests.get(url,headers= headers).text
            lxml_response = etree.HTML(response)
            detailurl_list = lxml_response.xpath('//div[@class="cont"]/p[1]/a/@href')
            print(len(detailurl_list))
            for detailurl in detailurl_list:
                detailurl = urllib.parse.urljoin(self.starturl, detailurl)
                print(detailurl)
                self.urlset.add(detailurl)
        return self.urlset

    def crawl_shici(self):
        '''
        爬取诗文
        :return: 诗文字典
        '''
        for i in range(self.startpage, self.endpage):
            url = urllib.parse.urljoin(self.starturl, '?p={0}'.format(i))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
            }
            response = requests.get(url, headers=headers).text
            lxml_response = etree.HTML(response)
            shici_block = lxml_response.xpath('//div[@class="left"]/div[@class="sons"]/div[@class="cont"]')
            for shici in shici_block:
                author=''
                yuanwen = ''
                title = shici.xpath('.//b/text()')
                title = get_frist(title)
                author_list = shici.xpath('.//p[@class="source"]//text()')
                if author_list:
                    for i  in author_list:
                        author += i
                yuanwen_list = shici.xpath('./div[@class="contson"]//text()')
                if yuanwen_list:
                    for i in yuanwen_list:
                        yuanwen += i
                self.content_dict['title'] = title
                self.content_dict['author'] = author
                self.content_dict['yuanwen'] = yuanwen
                yizhu_num = shici.xpath('.//div[@class="yizhu"]/img[3]/@id')[0][8:]
                # print(yizhu_num)
                self.request_yizhu(yizhu_num)
                yield self.content_dict

    def request_yizhu(self,yizhu_num):
        '''
        请求译文
        :param yizhu_num: 译文的id
        :return: 无
        '''
        yiwen = ''
        zhushi = ''
        yizhu_url = 'http://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id={0}&value=yizhu'.format(yizhu_num)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
        }
        response = requests.get(yizhu_url, headers=headers).text
        if response != '':
            lxml_response = etree.HTML(response)
            yiwen_list = lxml_response.xpath('//p/span[1]/text()')
            zhushi_list = lxml_response.xpath('//p/span[2]/text()')
            if yiwen_list:
                for i in yiwen_list:
                    yiwen += i
            if zhushi_list:
                for i in zhushi_list:
                    zhushi += i
        self.content_dict['yiwen'] = yiwen
        self.content_dict['zhushi'] = zhushi

    def crawl_author(self):
        '''
        爬取作者信息
        :return: 作者信息字典
        '''
        for i in range(self.startpage,self.endpage):
            url = urllib.parse.urljoin(self.starturl,'?p={0}'.format(i))
            print(url)
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
            }
            response = requests.get(url,headers= headers).text
            lxml_response = etree.HTML(response)
            author_list = lxml_response.xpath('//div[@class="sonspic"]/div[@class="cont"]')
            print (len(author_list))
            for author in author_list:
                author_name = author.xpath('.//b/text()')[0]
                author_content = author.xpath('.//p[2]/text()')[0]
                self.content_dict['author_name']=author_name
                self.content_dict['author_content']=author_content
                yield self.content_dict

if __name__ == "__main__":
    # url = 'http://so.gushiwen.org/type.aspx'
    url = 'http://so.gushiwen.org/authors/Default.aspx'
    crawl = CrawlUrl(url,1,2)
    for i in crawl.crawl_author():
        print(i)






