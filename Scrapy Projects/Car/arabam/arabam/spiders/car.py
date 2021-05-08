import scrapy


class CarSpider(scrapy.Spider):
    name = 'car'
    start_urls = ['https://www.arabam.com/ikinci-el/otomobil?take=50&page=1']
    page = 2
    def parse(self, response):
        List = response.css('tr.listing-list-item')
        for i in List:
            yield {'model': i.css('td.listing-modelname>h3>a::text').extract()[0],
                   'year': i.css('td.listing-text>div>a::text')[0].extract(),
                   'km': i.css('td.listing-text>div>a::text')[1].extract(),
                   'color': i.css('td.listing-text>div>a::text')[2].extract(),
                   'price': i.css('td.pl8>div>span>a::text').extract()[-1].strip(' TL'),
                   'province': i.css('td.listing-text>div>div>a>span::text')[0].extract(),
                   }
        next_page = 'https://www.arabam.com/ikinci-el/otomobil?page=' + str(CarSpider.page)

        if CarSpider.page <= 50:
            CarSpider.page += 1
            yield response.follow(next_page, callback=self.parse)
