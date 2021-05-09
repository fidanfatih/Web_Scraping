import scrapy


class SofifaSpider(scrapy.Spider):
    name = 'sofifa'
    # allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/?offset=0']

    def parse(self, response):
        List = response.css("tbody.list>tr")

        for i in List:
            href=i.css("td.col-name>a.tooltip::attr(href)").get()
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.css("div.pagination>a::attr(href)").extract()[-1] # next button hrefs

        # if next_page:
        #     url = response.urljoin(next_page)
        #     yield scrapy.Request(url)

        if next_page:
            url = response.urljoin(next_page)
            print('\n',url,'*'*100,'\n')
            yield response.follow(url, callback=self.parse)

    def parse_page(self, response):
        traits = [response.xpath(f'//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[11]/div/ul/li[{j}]/span/text()').get() for j in range(1,7)]
        traits = set([str(x) for x in traits])
        yield {"player_name": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/h1/text()').get(),
               "age": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div').re(' (\d\d)y.o. ')[0],
               "height":response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div').re(''' (\d'\d{1,2}\\\") ''')[0].replace('\\',''),
               "weight":response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div').re(' (\d{3})lbs')[0],
               "overall_rating": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/section/div/div[1]/div/span/text()').get(),
               "potential":  response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/section/div/div[2]/div/span/text()').get(),
               "value": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/section/div/div[3]/div').re('>(€\d*.*\d*[KM])<')[0],
               "wage":response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[1]/div/section/div/div[3]/div').re('>(€\d*.*\d*[KM])<')[0],
               "preferred_food": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[1]/text()').get(),
               "weak_food": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[2]/text()').get(),
               "skill_moves": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[3]/text()').get(),
               "reputation": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[4]/text()').get(),
               "work_rate": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[5]/span/text()').get(),
               "body_type": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[6]/span/text()').get(),
               "real_face": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[7]/span/text()').get(),
               "release_clause": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[8]/span/text()').get(),
               "id": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/ul/li[9]/text()').get(),
               "position": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/ul/li[2]/span/text()').get(),
               "jersey_num": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/ul/li[3]/text()').get(),
               "contract_valid": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/ul/li[5]/text()').get(),
               "crossing": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[4]/div/ul/li[1]/span[1]/text()').get(),
               "finishing": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[4]/div/ul/li[2]/span[1]/text()').get(),
               "heading_accuracy": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[4]/div/ul/li[3]/span[1]/text()').get(),
               "short_passing": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[4]/div/ul/li[4]/span[1]/text()').get(),
               "volleys": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[4]/div/ul/li[5]/span[1]/text()').get(),
               "dribbling": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[5]/div/ul/li[1]/span[1]/text()').get(),
               "curve": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[5]/div/ul/li[2]/span[1]/text()').get(),
               "fk_accuracy": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[5]/div/ul/li[3]/span[1]/text()').get(),
               "long_passing": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[5]/div/ul/li[4]/span[1]/text()').get(),
               "ball_control": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[5]/div/ul/li[5]/span[1]/text()').get(),
               "acceleration": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[6]/div/ul/li[1]/span[1]/text()').get(),
               "sprint_speed": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[6]/div/ul/li[2]/span[1]/text()').get(),
               "agility": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[6]/div/ul/li[3]/span[1]/text()').get(),
               "reactions": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[6]/div/ul/li[4]/span[1]/text()').get(),
               "balance": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[6]/div/ul/li[5]/span[1]/text()').get(),
               "shot_power": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[7]/div/ul/li[1]/span[1]/text()').get(),
               "jumping": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[7]/div/ul/li[2]/span[1]/text()').get(),
               "stamina": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[7]/div/ul/li[3]/span[1]/text()').get(),
               "strength": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[7]/div/ul/li[4]/span[1]/text()').get(),

               "long_shots": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[7]/div/ul/li[5]/span[1]/text()').get(),
               "aggression": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[1]/span[1]/text()').get(),
               "interceptions": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[2]/span[1]/text()').get(),
               "positioning": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[3]/span[1]/text()').get(),
               "vision": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[4]/span[1]/text()').get(),
               "penalties": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[5]/span[1]/text()').get(),
               "composure": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[8]/div/ul/li[6]/span/text()').get(),

               "defensive_awareness": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[9]/div/ul/li[1]/span[1]/text()').get(),
               "standing_tackle": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[9]/div/ul/li[2]/span[1]/text()').get(),
               "sliding_tackle": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[9]/div/ul/li[3]/span[1]/text()').get(),
               "gk_diving": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[10]/div/ul/li[1]/span/text()').get(),
               "gk_handling": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[10]/div/ul/li[2]/span/text()').get(),
               "gk_kicking": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[10]/div/ul/li[3]/span/text()').get(),
               "gk_positioning": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[10]/div/ul/li[4]/span/text()').get(),
               "gk_reflexes": response.xpath('//*[@id="list"]/div[2]/div/div/div[1]/div[1]/div[10]/div/ul/li[5]/span/text()').get(),
               "traits":[i for i in traits if i != 'None']
               }

