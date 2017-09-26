import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazonpider'
    start_urls = ['https://www.amazon.com.br/gp/registry/wishlist/3DA4I0ZLH8ADW']

    def parse(self, response):
      books_root = response.css("#item-page-wrapper")
      books = books_root.xpath('//div[re:test(@id, "itemMain_*")]')
      for book in books:
        book_info = book.xpath('.//div[re:test(@id, "itemInfo_*")]')
        title = self.strformat(book_info.xpath('.//a[re:test(@id, "itemName_*")]/text()').extract_first())
        authors_format = reduce(lambda a, b: a+b, map(lambda x: x.strip() ,book_info.xpath('.//div[@class="a-row a-size-small"]/text()').extract()))
        price = self.strformat(book_info.xpath('.//span[re:test(@id, "itemPrice_*")]/text()').extract_first())

        yield {'Title':title, 'Info':authors_format, 'Last price':price }

      pagination_ref = response.css("#wishlistPagination")
      next_page = pagination_ref.xpath('.//li[@class="a-last"]//a//@href').extract_first()
      if next_page:
        yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def strformat(self, data):
      if data != None:
        return data.strip()

