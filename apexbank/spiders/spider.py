import scrapy

from scrapy.loader import ItemLoader

from ..items import ApexbankItem
from itemloaders.processors import TakeFirst


class ApexbankSpider(scrapy.Spider):
	name = 'apexbank'
	start_urls = ['https://www.apexbank.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="pagination-next alignright"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//header/h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=ApexbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
