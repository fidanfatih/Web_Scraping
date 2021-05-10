import scrapy

class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    # allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com.tr/Hotels-g298656-Ankara-Hotels.html']

    page = 30
    def parse(self, response):
        # hrefs = response.css('a.property_title.prominent::attr(href)').extract()
        # or
        # hrefs = response.css("div.listing_title a::attr(href)").extract()
        # or
        hrefs = response.css("div.listing_title>a::attr(href)").extract()

        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.css("a.nav.next.ui_button.primary::attr(href)").extract()[0] # next button hrefs

        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url)

    def parse_page(self, response):
        yield {
               "otel_name_css": response.css('div._1vnZ1tmP>h1::text').get(),
               "otel_name_xpath": response.xpath('//*[@id="HEADING"]/text()').get(),
               "rate_css": response.css('div.kVNDLtqL>span::text').get(),
               "rate_xpath":  response.xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/span/text()').get(),
               "review_count": response.xpath('//*[@id="component_4"]/div/div[1]/div[1]/div[2]/a/span[2]/text()').get(),
               "price_xpath": response.xpath('//*[@id="component_25"]/div[2]/div[2]/div[3]/div[1]/div[1]/text()').get(),
               "address": response.xpath(
            '//*[@id="component_4"]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/span[2]/span/text()').get(),
               }