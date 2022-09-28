import time
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class UsersSpider(scrapy.Spider):
    name = 'quote'
    start_urls = [
        'https://www.strava.com/login'
    ]

    def parse(self, response):
        token = response.css('meta::attr(content)').extract_first()
        print(token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'anika.bhad@ncsu.edu',
            'password': 'Password'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        # Number of pages that are going to be crawled
        depth = 10
        # Loop going from 1-10 crawling each page refrenced
        for pageNumber in range(depth):
            # yield response.follow(x,callback=self.parse) is the
            # function to crawl the page. This means each page in this loop will be crawled
            yield response.follow('https://www.strava.com/athletes/search?gsf=1&page=' + str(pageNumber + 1) + '&page_'
                                  + 'uses_modern_javascript=true&text=&utf8=%E2%9C%93', callback=self.parse)
        all_users = response.css('li.row')
        for user in all_users:
            name = user.css('div.text-headline::text').extract()
            location = user.css('div.location::text').extract()

            objToYield = {'name': name, 'location': location, 'crawlTime': time.time()}
            yield objToYield


