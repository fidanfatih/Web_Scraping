"""
https://www.youtube.com/watch?v=Pu3gmdWsLYc&ab_channel=codeRECODE

CTRL+SHIFT+I
click >> Disable cache
CTRL+SHIFT+P
type >> Disable Javascript
refresh page >> if page is gone, Javascript is used in website
type >> Enable Javascript
refresh page >> page will be seemed.
click >> XHR
click >> second row(below Setting)
request headers > copy all dictionary items to headers

"""

import scrapy
import json


class NtschoolsSpider(scrapy.Spider):
    name = 'ntschools'
    start_urls = ['https://directory.ntschools.net/#/schools']
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,fil;q=0.7",
        'Referer': "https://directory.ntschools.net/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "Fetch",
    }

    def parse(self, response):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'    # copy link address of GetAllSchools
        request = scrapy.Request(url,
                                 callback=self.parse_api,
                                 headers=self.headers)
        yield request

    def parse_api(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        raw_data = response.body
        data = json.loads(raw_data)

        for school in data:
            school_code = school['itSchoolCode']
            school_url = base_url + school_code
            request = scrapy.Request(school_url,
                                     callback=self.parse_school,
                                     headers=self.headers)
            yield request

    def parse_school(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        yield {
            'Name': data['name'],
            'Religion': data['religion'],
            'PhysicalAddress_1': data['physicalAddress']['displayAddress'],
            'PostalAddress': data['postalAddress']['displayAddress'],
            'Email': data['mail'],
            'Phone': data['telephoneNumber']
        }