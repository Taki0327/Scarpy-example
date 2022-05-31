import scrapy

class Nuitnews(scrapy.Spider):
    name = 'nuitnews'
    i=1
    start_urls = [
        'http://news.niit.edu.cn/4004/list.htm',
    ]
    def parse(self, response):
        for quote in response.xpath('//div[@id="wp_news_w6"]/ul/li'):
            newmeta={
                'title' : quote.css('span.news_title a::text').get(),
                'time' : quote.css('span.news_meta::text').get(),
                'text' :  ""
            }
            url = quote.css('span.news_title a::attr(href)').get()
            yield response.follow(url,callback=self.parse2,meta=newmeta)
        next_page = response.xpath('//*[@id="wp_paging_w6"]/ul/li[2]/a[3]/@href').get()
        if next_page is not None and self.i<3:
            self.i=self.i+1
            yield response.follow(next_page, self.parse)
    def parse2(self, response):
        newmeta=response.meta
        newmeta["text"]=response.css('div.wp_articlecontent::text').getall()
        yield newmeta