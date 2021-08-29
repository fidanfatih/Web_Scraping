import scrapy
#scrapy crawl autoscout24 -o autoscout_data.json
#scrapy crawl autoscout24 -o autoscout_data.csv

class Autoscout24Spider(scrapy.Spider):
    name = 'autoscout24'
    start_urls = ['https://www.autoscout24.com']

    countries = {
                 'NL':'Netherlands',
                 # 'D':'Germany',
                 # 'F':'France',
                 }
    makes =['audi',
            'bmw','ford',
            'mercedes-benz','opel','volkswagen',
            'renault','citroen','chevrolet','dacia',
            'fiat','honda','hyundai','kia','mazda',
            'peugeot','skoda','toyota','tesla','volvo',
            ]
    fuel_types= {'B':'Gasoline',
                 'D':'Diesel', 'E':'Electric', '2':'Electric/Gasoline', '3':'Electric/Diesel', 'C%2CH%2CL%2CM%2CO':'Other',
                 }
    body_types= {
        '1':'Compact','2':'Convertible','3':'Coupe','4':'Off-Road/Pick-up','5':'Station wagon',
        '6':'Sedans',
        '7':'Other','12':'Van','13':'Transporter',
    }
    gears={'A':'Automatic',
           'M':'Manuel','S':'Semi-automatic',
           }
    pages = range(1,21)
    country=''
    body_type=''
    fuel_type=''
    gear_type=''
    url=''
    sub_url=''

    def start_requests(self):
        for k1,v1 in self.countries.items():
            self.country = v1
            for make in self.makes:
                for k2, v2 in self.fuel_types.items():
                    self.fuel_type = v2
                    for k3, v3 in self.body_types.items():
                        self.body_type = v3
                        for k4, v4 in self.gears.items():
                            self.gear_type = v4
                            for page in self.pages:
                                self.url=f'https://www.autoscout24.com/lst/{make}?sort=standard&desc=0&gear={k4}&fuel={k2}&uproperties=N%2CU&size=20&page={page}&cy=NL&fregto=2021&fregfrom=2010&body={k3}&atype=C&recommended_sorting_based_id=3be38a31-5629-4278-9e4d-8f34145baff4&'
                                yield scrapy.Request(
                                    url=self.url,
                                    callback=self.parse
                                )

    def parse(self, response):
        for hrefs in response.xpath("//a[@data-item-name='detail-page-link']"):  #https://docs.scrapy.org/en/latest/topics/selectors.html
            self.sub_url = response.urljoin(hrefs.xpath('.//@href').get())
            yield scrapy.Request(
                url=self.sub_url,
                callback=self.extract_data,
            )

    def extract_data(self, response):
        state = {
            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[1]/text()").get(): response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[1]/a/text()").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[2]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[2]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[3]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[4]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[5]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[5]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[6]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[6]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[7]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[7]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[8]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[8]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dt[9]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[1]/dl/dd[9]/text())").get(),
        }

        drive = {
            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[1]/text()").get(): response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[1]/a/text()").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[2]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[2]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[3]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[3]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[4]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[4]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[5]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[5]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[6]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[6]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[7]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[7]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[8]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[8]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dt[9]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[3]/dl/dd[9]/text())").get(),
        }

        environment = {
            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[1]/text()").get(): response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[1]/a/text()").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[2]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[2]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[3]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[3]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[4]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[4]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[5]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[5]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[6]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[6]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[7]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[7]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[8]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[8]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dt[9]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[2]/div/div/div/div[1]/dl/dd[9]/text())").get(),
        }

        properties = {
            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[1]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[1]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[2]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[2]/a/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[3]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[3]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[4]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[4]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[5]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[5]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[6]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[6]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[7]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[7]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[8]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[8]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[9]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[9]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[10]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[10]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[11]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[11]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[12]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[12]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[13]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[13]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[14]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[14]/text())").get(),

            response.xpath(
                "/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dt[15]/text()").get(): response.xpath(
                "normalize-space(/html/body/div[1]/main/div[3]/div/div/div[7]/div[2]/div[1]/div[2]/dl/dd[15]/text())").get(),
        }

        # description = response.xpath("(//div[@class='sc-grid-col-6 sc-grid-col-s-12'])/div[1]/text()").getall()

        yield {
            'country': self.country,
            'title': response.xpath("(//span[@class='cldt-detail-makemodel sc-ellipsis'])/text()").get(),
            'short_description': response.xpath("(//span[@class='cldt-detail-version sc-ellipsis'])/text()").get(),
            'price': response.xpath("normalize-space((//div[@class='cldt-price '])[2]/h2/text())").re('(€ \d*\,*\d*).-')[0],
            'km': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()").get(),
            'registration': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()")[1].get(),
            'kw': response.xpath("(//span[@class='sc-font-l cldt-stage-primary-keyfact'])/text()")[2].get(),
            'hp': response.xpath("(//div[@class='cldt-stage-basic-data'])/div[3]/span[2]/text()").get(),
            'transmission': response.xpath("(//span[@class='sc-font-s cldt-stage-att-description'])/text()").get(),
            # state
            'type': state['Type'] if 'Type' in state.keys() else 'None',
            'previous_owners': state['Previous Owners'] if 'Previous Owners' in state.keys() else 'None',
            'next_inspection': state['Next Inspection'] if 'Next Inspection' in state.keys() else 'None',
            'inspection_new': state['Inspection new'] if 'Inspection new' in state.keys() else 'None',
            'warranty': state['Warranty'] if 'Warranty' in state.keys() else 'None',
            'full_service': '1' if 'Full Service' in state.keys() else '0',
            'last_service_date': state['Last Service Date'] if 'Last Service Date' in state.keys() else 'None',
            'non_smoking_vehicle': '1' if 'Non-smoking Vehicle' in state.keys() else '0',
            'last_timing_belt_service_date': state['Last Timing Belt Service Date'] if 'Last Timing Belt Service Date' in state.keys() else 'None',
            # drive
            'gearing_type': drive['Gearing Type'] if 'Gearing Type' in drive.keys() else 'None',
            'gears': drive['Gears'] if 'Gears' in drive.keys() else 'None',
            'gear_type': self.gear_type,
            'displacement': drive['Displacement'] if 'Displacement' in drive.keys() else 'None',
            'Cylinders': drive['Cylinders'] if 'Cylinders' in drive.keys() else 'None',
            'weight': drive['Weight'] if 'Weight' in drive.keys() else 'None',
            'drive chain': drive['Drive chain'] if 'Drive chain' in drive.keys() else 'None',
            # enviroment
            'fuel': environment['Fuel'] if 'Fuel' in environment.keys() else 'None',
            'fuel_type': self.fuel_type,
            'consumption_comb': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[1]/text()").get(),
            'consumption_city': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[2]/text()").get(),
            'consumption_country': response.xpath("(//div[@class='cldt-data-section sc-grid-col-s-12'])/dl/dd[2]/div[3]/text()").get(),
            'co2_emission': environment['CO2 Emission'] if 'CO2 Emission' in environment.keys() else 'None',
            'emission_class': environment['Emission Class'] if 'Emission Class' in environment.keys() else 'None',
            'emission_label': environment['Emission Label'] if 'Emission Label' in environment.keys() else 'None',
            # properties
            'make': properties['Make'] if 'Make' in properties.keys() else 'None',
            'model': properties['Model'] if 'Model' in properties.keys() else 'None',
            'offer_number': properties['Offer Number'] if 'Offer Number' in properties.keys() else 'None',
            'first_registration': properties['First Registration'] if 'First Registration' in properties.keys() else 'None',
            'body_color': properties['Body Color'] if 'Body Color' in properties.keys() else 'None',
            'paint_type': properties['Paint Type'] if 'Paint Type' in properties.keys() else 'None',
            'body_color_original': properties['Body Color Original'] if 'Body Color Original' in properties.keys() else 'None',
            'upholstery': properties['Upholstery'] if 'Upholstery' in properties.keys() else 'None',
            'body_type': self.body_type,
            'body': properties['Body'] if 'Body' in properties.keys() else 'None',
            'nr_of_doors': properties['Nr. of Doors'] if 'Nr. of Doors' in properties.keys() else 'None',
            'nr_of_seats': properties['Nr. of Seats'] if 'Nr. of Seats' in properties.keys() else 'None',
            'model_code': properties['Model Code'] if 'Model Code' in properties.keys() else 'None',
            'country_version': properties['Country version'] if 'Country version' in properties.keys() else 'None',

            # 'description': '|'.join([i.strip('\n') for i in description if i != '\n']),
        }