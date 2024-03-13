import unittest
from scrapy.http import TextResponse
from smartphone_spider import SmartphoneSpider


class TestSmartphoneSpider(unittest.TestCase):
    def test_parse_smartphone(self):
        spider = SmartphoneSpider()
        html_content = """
        <html>
            <body>
                <h1>Смартфон 1</h1>
                <div class="b1e1">
                    <span>Версия ОС</span>
                    <div><span>Android 11</span></div>
                </div>
            </body>
        </html>
        """
        response = TextResponse(url='https://www.example.com', body=html_content, encoding='utf-8')
        parsed_item = list(spider.parse_smartphone(response))
        self.assertEqual(len(parsed_item), 1)
        self.assertEqual(parsed_item[0]['name'], 'Смартфон 1')
        self.assertEqual(parsed_item[0]['os_version'], 'Android 11')


if __name__ == '__main__':
    unittest.main()
