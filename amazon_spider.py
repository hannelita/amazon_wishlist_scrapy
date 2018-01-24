import scrapy
import logging

class AmazonSpider(scrapy.Spider):
    name = 'amazonspider'
    start_urls = ['https://www.amazon.com.br/gp/registry/wishlist/3DA4I0ZLH8ADW']

    def parse(self, response):
      books_root = response.css("#item-page-wrapper")
      books = books_root.xpath('//div[re:test(@id, "itemMain_*")]')
      for book in books:
        book_info = book.xpath('.//div[re:test(@id, "itemInfo_*")]')
        title = self.strformat(book_info.xpath('.//a[re:test(@id, "itemName_*")]/text()').extract_first())
        authors_format = ''
        if book_info.xpath('.//div[@class="a-row a-size-small"]/span/text()'):
          authors_format = reduce(lambda a, b: a+b, map(lambda x: x.strip(), book_info.xpath('.//div[@class="a-row a-size-small"]/span/text()').extract()))
        price = self.strformat(book_info.xpath('.//span[re:test(@id, "itemPrice_*")]//span/text()').extract_first())

        yield {'Title':title, 'Info':authors_format, 'Last price':price }

      next_page_ref = response.css('#sort-by-price-load-more-items-url').xpath('.//@value').extract_first()
      next_page = "https://www.amazon.com.br" + next_page_ref
      if "lek=&" not in next_page:
        yield scrapy.Request(next_page, callback=self.parse)


    def strformat(self, data):
      if data != None:
        return data.strip()

