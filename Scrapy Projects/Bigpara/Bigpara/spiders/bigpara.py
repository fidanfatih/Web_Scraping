import scrapy


class BigparaSpider(scrapy.Spider):
    name = 'bigpara'
    # allowed_domains = ['bigpara.com']
    start_urls = ['https://bigpara.hurriyet.com.tr/bilgi/gerekli-linkler/']

    def parse(self, response):
        List = response.css('div.column>ul')
        for i in List:
            yield {'Bank': i.css('li::text').extract()[0],
                   'Web_Site': i.css('li>a::attr(href)').extract()[0],
                   }
