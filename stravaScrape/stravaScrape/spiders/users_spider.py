import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuoteSpider(scrapy.Spider) :
    name = 'strava'
    start_urls = [
        'https://www.strava.com/login'
    ]

    def parse(self, response):
        token = response.xpath("//meta[@name='csrf-token']/@content").extract_first()
        print(token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'anika.bhad@gmail.com',
            'password': 'Password'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
        # items = QuotetutorialItem()

        all_div_quote = response.css('div.quote')

        for quote in all_div_quote:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            #
            # items['title'] = title
            # items['author'] = author
            # items['tag'] = tag

            # yield items