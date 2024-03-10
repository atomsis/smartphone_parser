import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class SmartphoneSpider(scrapy.Spider):
    name = 'smartphone'
    allowed_domains = ['ozon.ru']
    start_urls = ['https://www.ozon.ru/category/telefony-i-smart-chasy-15500/?sorting=rating']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        sel = Selector(text=self.driver.page_source)
        smartphone_links = sel.css('.e3f44fce2f').css('a::attr(href)').extract()[:100]  # Выбираем первые 100 смартфонов
        for link in smartphone_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(absolute_url, callback=self.parse_smartphone)

    def parse_smartphone(self, response):
        yield {
            'name': response.css('h1::text').get(),
            'os_version': response.css('.b1e1').xpath(
                '//span[contains(text(), "Версия ОС")]/following-sibling::div/span/text()').get()
        }

    def closed(self, reason):
        self.driver.quit()
