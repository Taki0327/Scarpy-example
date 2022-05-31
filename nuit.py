import scrapy

class News(scrapy.Item):
    title=scrapy.Field()
    time=scrapy.Field()
    text=scrapy.Field()
class Nuitnews(scrapy.Spider):
    name = 'nuitnews'
    i=1
    start_urls = [
        'http://news.niit.edu.cn/4004/list.htm',
    ]
    def parse(self, response):
        new=News()
        for quote in response.xpath('//div[@id="wp_news_w6"]/ul/li'):
            new["title"]=quote.css('span.news_title a::text').get()
            new["time"]=quote.css('span.news_meta::text').get()
            url = quote.css('span.news_title a::attr(href)').get()
            yield response.follow(url,callback=self.parse2,meta={"new":new})
            yield {
                'title' : new["title"],
                'time' : new["time"],
                'text' :  new["text"]
            }
            #$self.txt=""
        next_page = response.xpath('//*[@id="wp_paging_w6"]/ul/li[2]/a[3]/@href').get()
        if next_page is not None and self.i<3:
            self.i=self.i+1
            yield response.follow(next_page, self.parse)
    def parse2(self, response):
        new=response.meta["new"]
        new["text"]=response.css('div.wp_articlecontent::text').getall()
        yield new