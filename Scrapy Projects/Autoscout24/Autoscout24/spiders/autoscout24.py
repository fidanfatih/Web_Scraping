import scrapy

class Autoscout24Spider(scrapy.Spider):
    name = 'autoscout24'
    start_urls = ['https://www.autoscout24.com/lst/audi?sort=standard&desc=0&ustate=N%2CU&size=20&page=1&cy=NL&fregto=2021&fregfrom=2010&atype=C&recommended_sorting_based_id=39d7a477-90b4-4239-aafc-f972717695e0&']
    page_num = 1

    countries = {'NL':'Netherlands','D':'Germany','F':'France'}
    makes =['Audi','BMW','Ford', 'Mercedes-Benz','Opel','Volkswagen','Renault','Citroen','Chevrolet','Dacia','Fiat','Honda','Hyundai','Kia','Peugeot','Skoda','Toyota','Volvo']
    pages = range(1,21)
    country=''

    def start_requests(self):
        for k,v in self.countries.items():
            self.country = v
            for make in self.makes:
                for page in self.pages:
                    yield scrapy.Request(
                        url= f'https://www.autoscout24.com/lst/{make}?sort=standard&desc=0&ustate=N%2CU&size=20&page={page}&cy={k}&fregto=2021&fregfrom=2010&atype=C&recommended_sorting_based_id=39d7a477-90b4-4239-aafc-f972717695e0&',
                        callback=self.parse
                    )

    def parse(self, response):
        with open('exported_page.html', 'wb') as f:
            f.write(response.body)
        for hrefs in response.xpath("//a[@data-item-name='detail-page-link']"):  #https://docs.scrapy.org/en/latest/topics/selectors.html
            sub_url = response.urljoin(hrefs.xpath('.//@href').get())
            yield scrapy.Request(
                url=sub_url,
                callback=self.extract_data
            )

    def extract_data(self, response):
        description = response.xpath("(//div[@class='sc-grid-col-6 sc-grid-col-s-12'])/div[1]/text()").getall()
        yield {
            'country': self.country,
            'title': response.xpath("(//span[@class='cldt-detail-makemodel sc-ellipsis'])/text()").get(),
            'short_description': response.xpath("(//span[@class='cldt-detail-version sc-ellipsis'])/text()").get(),
            'price': response.xpath("normalize-space((//div[@class='cldt-price '])[2]/h2/text())").get().split(',')[0],
            'km': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()").get(),
            'registration': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()")[1].get(),
            'kw': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()")[2].get(),
            'hp':response.xpath("(//div[@class='cldt-stage-basic-data'])/div[3]/span[2]/text()").get(),
            'transmission':response.xpath("(//span[@class='sc-font-s cldt-stage-att-description'])/text()").get(),
            'type':response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[1]/dl/dd[1]/a/text()").get(),
            'previous_owners': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[1]/dl/dd[2]/text())").get(),
            'next_inspection':  response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[1]/dl/dd[3]/text())").get(),
            'make':response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[1]/text())").get(),
            'model': response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[2]/a/text()").get(),
            'offer_number': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[3]/text())").get(),
            'first_registration': response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[4]/a/text()").get(),
            'body_color': response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[5]/a/text()").get(),
            'paint_type': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[6]/text())").get(),
            'upholstery': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[7]/text())").get(),
            'body': response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[8]/a/text()").get(),
            'nr.of_doors': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[9]/text())").get(),
            'nr.of_seats': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[10]/text())").get(),
            'model_code': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-right'])[1]/dl/dd[11]/text())").get(),
            'gearing_type': response.xpath("(//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[1]/a/text()").get(),
            'gears': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[2]/text())").get(),
            'displacement': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[3]/text())").get(),
            'cylinders': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[4]/text())").get(),
            'weight': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[5]/text())").get(),
            'drive_chain': response.xpath("normalize-space((//div[@class='cldt-categorized-data cldt-data-section sc-pull-left'])[2]/dl/dd[6]/text())").get(),
            'fuel': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[1]/a/text()").get(),
            'consumption_comb': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[1]/text()").get(),
            'consumption_city': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[2]/text()").get(),
            'consumption_country': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[3]/text()").get(),
            'co2_emission': response.xpath("normalize-space((//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[3]/text())").get(),
            'emission_class': response.xpath("normalize-space((//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[4]/text())").get(),
            'emission_label': response.xpath("normalize-space((//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[5]/text())").get(),
            'comfort_convenience': response.xpath("(//div[@class='cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left'])[1]/span/text()").getall(),
            'entertainment_media': response.xpath("(//div[@class='cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left'])[2]/span/text()").getall(),
            'extras': response.xpath("(//div[@class='cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left'])[3]/span/text()").getall(),
            'safety_security': response.xpath("(//div[@class='cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left'])[4]/span/text()").getall(),
            'phone_number': response.xpath("//div[@class='cldt-call-btn-m']/text()").get(),
            # 'description': '|'.join([i.strip('\n') for i in description if i != '\n']),
        }