import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]


    def parse(self, response):

        # get the books section
        books = response.css("article.product_pod")

        for book in books:
            # extract the url of the page of each book
            book_page_url = book.css('h3 a').attrib['href']

            # if the url does not contain the full relative url, complete it
            # note: you get the data of page 1 if you don't check for it
            if "catalogue/" not in book_page_url:
                book_page_url = "catalogue/" + book_page_url
            
            # get the book page and scrape it with parse_book_page() method
            yield scrapy.Request("https://books.toscrape.com/" + book_page_url, callback = self.parse_book_page)



        next_page_url = response.css("ul.pager li.next a").attrib['href']

        # if there is next page, call parse method for it
        if next_page_url is not None:

            # if the url does not contain the full relative url, complete it
            # note: you get the data of page 1 if you don't check for it
            if "catalogue/" not in next_page_url:
                next_page_url = "catalogue/" + next_page_url

            next_page_url = "https://books.toscrape.com/" + next_page_url 
            
            yield response.follow(next_page_url, callback = self.parse)


    def parse_book_page(self, response):
        rows = response.css("table.table-striped tr")

        yield {
            "category" : response.xpath("//li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            "description" : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            "upc" : rows[0].css("td::text").get(),
            "product_type" : rows[1].css("td::text").get(),
            "price_excl_tax" : rows[2].css("td::text").get(),
            "price_incl_tax" : rows[3].css("td::text").get(),
            "tax" : rows[4].css("td::text").get(),
            "availability" : rows[5].css("td::text").get(),
            "n_reviews" : rows[6].css("td::text").get(),
        }