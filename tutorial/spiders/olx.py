import scrapy

class PeterParkerSpider(scrapy.Spider):
    name = "olx"

    def start_requests(self):
        urls = [
            'https://www.olx.com.pk/items/q-yamaha-ybr-g'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        listings = response.css("article._7e3920c1")
        for listing in listings:
            image_url = listing.css("div.ee2b0479 picture._219b7e0a img._943b7102::attr(src)").get()
            title = listing.css("div._41d2b9f3 div.a5112ca8::text").get()
            price = listing.css("div._52497c97 span::text").get()
            location = listing.css("div._4dbba078 div._2fc90438 span._424bf2a8::text").get()
            last_updated = listing.css("div._2fc90438 span._2e28a695 span::text").get()

            yield {"image_url":image_url, "title":title, "price":price, "location":location, "last_updated":last_updated}

        next_page = response.css("a._95dae89d::attr(href)").get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
