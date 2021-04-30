import scrapy
import re


class TrendyolSpider(scrapy.Spider):
    name = 'trendyol'
    # allowed_domains = ['trendyol.com']
    start_urls = ['https://www.trendyol.com/tv-goruntu-ses-sistemleri-x-c104035?pi=1']
    page = 2

    def error_check(self, i, statement, j):
        try:
            i.css(statement)[j].extract()
        except:
            return None
        return i.css(statement)[j].extract()

    def get_rating(self,i):
        rating=0
        all_star = i.css('div.star-w>div.full::attr(style)').getall()
        for star in all_star:
            rating += int(re.search(r"\d{1,3}", star).group())
        return str(rating/100)

    def parse(self, response):
        List = response.css('div.p-card-wrppr')
        for i in List:
            yield {'brand': self.error_check(i,'div.prdct-desc-cntnr-ttl-w>span::text',0),
                   'model': self.error_check(i,'div.prdct-desc-cntnr-ttl-w>span::text',1),
                   'rating': self.get_rating(i),
                   'ratingCount': self.error_check(i,'div.ratings>span::text',1),
                   'price': self.error_check(i,'div.prc-box-sllng::text',0),
                   'campaign': self.error_check(i,'div.prmtn-ttl::text',0),
                   'discounted_price': self.error_check(i, 'div.prc-box-dscntd::text',0),
                   }
        next_page = 'https://www.trendyol.com/tv-goruntu-ses-sistemleri-x-c104035?pi=' + str(TrendyolSpider.page)

        if TrendyolSpider.page <= 208:
            TrendyolSpider.page += 1
            yield response.follow(next_page, callback=self.parse)
