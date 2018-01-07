from crawl_url import CrawlUrl
from crawl_save import SaveSpider

def main():
    '''执行函数'''
    save_author = SaveSpider('127.0.0.1',27017,'fjdal','author')
    save_shici = SaveSpider('127.0.0.1',27017,'fjdal','shici')
    content_url = 'http://so.gushiwen.org/type.aspx'
    content_crawl = CrawlUrl(content_url,1,2)
    for j in content_crawl.crawl_shici():
        print (j)
        save_shici.content_insert(j)

    author_url = 'http://so.gushiwen.org/authors/Default.aspx'
    author_crawl = CrawlUrl(author_url, 1, 2)
    for i in author_crawl.crawl_author():
        print(i)
        save_author.content_insert(i)


if __name__ == '__main__':
    main()