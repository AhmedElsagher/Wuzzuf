import scrapy
import json
from flatten_json import flatten

class ProfileSpider(scrapy.Spider):
    name = "profile"

    def start_requests(self):
        # base_url = "https://wuzzuf.net/directory/members/a"
        urls = [
            'https://wuzzuf.net/directory/members/a?p=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.selector.xpath('//div[@class="col-md-6"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_page)
        next_page =  response.selector.xpath('//ul/li/a/span[contains(text(),"Next")]')
        if next_page:
            page = response.request.url.split("=")[1]
            next_page_number = int(page) + 1
            url =  response.request.url.split("=")[0] +"="+ str(next_page_number)
            if next_page:
                yield  scrapy.Request(url, callback=self.parse)

    def parse_page(self,response):
        script = response.selector.xpath("//script")[0]
        script = script.get().split("\n")[4].split("initialStoreState = ")[1][:-1]
        script = json.loads(script)
        # script = flatten(script)
        yield script
