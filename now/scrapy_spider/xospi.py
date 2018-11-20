import scrapy
import re
import base64


class QuotesSpider(scrapy.Spider):
    name = "xxoo"

    def hehe(self, response):
        maxpage = int(re.findall('current-comment-page">\[(\d*?)\]', response.body)[0])
        urls = ['http://jandan.net/ooxx/page-' + str(i) + "#comments" for i in range(maxpage,0,-1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
        yield scrapy.Request(url="http://jandan.net/ooxx/",callback=self.hehe,headers=headers,encoding='utf-8')

    def down(self,response):
        tmpname = response.url[response.url.rfind('/') + 1:]
        with open('./pics/' + tmpname, 'wb') as f:
            f.write(response.body)

    def parse(self, response):
        total = re.findall('img-hash">.*?<', response.text)
        for j in total:
            tmp = base64.b64decode(j[10:-1]).decode('utf-8')
            tmp = re.sub('cn/.*?/','cn/large/', tmp)
            tmp = 'http:' + tmp
            yield scrapy.Request(tmp,callback=self.down)
