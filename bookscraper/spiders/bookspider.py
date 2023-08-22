import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]


    def parse(self, response):

        # get the books section
        books = response.css("article.product_pod")

        for book in books:
            yield {
                'name' : book.css("h3 a::text").get(),
                'price' : book.css("div.product_price p.price_color::text").get(),
                'url' : book.css('h3 a').attrib['href']
            }

        next_page_url = response.css("ul.pager li.next a").attrib['href']

        if next_page_url is not None:
            yield response.follow(next_page_url, callback = self.parse)
