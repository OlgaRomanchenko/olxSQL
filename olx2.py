import csv
import random
from less23 import *
from requests_html import HTMLSession


class OlxParser:

    def __init__(self):
        self.start_url = 'https://www.olx.ua/'
        self.category_xpath = '//li/a[@data-id]/@href'
        self.proxies = []
        self.agents = []
        self.session = HTMLSession()
        self.result_file = 'olx_ads.csv'
        self.set_all_proxies()
        self.set_all_agents()

        self.fieldnames = ['ad_title', 'ad_date', 'ad_price',
                           'ad_photo', 'ad_link', 'ad_city']
        print('Crawler Initialized')

    def set_all_proxies(self):
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            self.proxies = [p.strip() for p in f if p.strip()]

    def set_all_agents(self):
        with open('ua.txt', 'r', encoding='utf-8') as f:
            self.agents = [x.strip() for x in f if x.strip()]

    def get_random_proxy(self):
        random_proxy = random.choice(self.proxies)
        print('get_random_proxy', random_proxy)
        return {'http': f'socks5://{random_proxy}',
                'https': f'socks5://{random_proxy}'}

    def get_random_headers(self):
        print('get_random_headers')
        return {'User-Agent': random.choice(self.agents)}

    def get_category_links(self):
        headers = self.get_random_headers()
        response = self.session.get(self.start_url, headers=headers)
        links = response.html.xpath(self.category_xpath)
        print('get_category_links', links)
        return links

    def run(self):
        links = self.get_category_links()

        for link in links:
            headers = self.get_random_headers()
            resp = self.session.get(link, headers=headers)
            self.get_ads(resp)

    def get_ads(self, response):
        ad_blocks = response.html.xpath('//div[@class="offer-wrapper"]')
        ad_category =response.html.xpath('//span[@class="link"]')
        for a in ad_category:
            try:
                ab=Category.get(name=a.text)

            except DoesNotExist:
                ab = Category.create(name=a.text)

        for ad in ad_blocks:

            try:

                ad_title = ad.xpath('//h3')[0].text
                ad_photo = ad.xpath('//img/@src')[0]
                ad_link = ad.xpath('//h3/a/@href')[0]
                ad_city = ad.xpath('//p[@class="lheight16"]/small[1]')[0].text


                b = Announcement.create(title=ad_title,
                                        photo=ad_photo,
                                        link=ad_link,
                                        city=ad_city,
                                        category=ab)

                print(b)

            except Exception:
                pass


if __name__ == '__main__':
    olx = OlxParser()
    olx.run()

