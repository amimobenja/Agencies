from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from agencies.items import AgenciesItem

class AgenciesLoader(XPathItemLoader):
	default_item_class = AgenciesItem
	default_input_processor = MapCompose(lambda x: x.strip())
	default_output_processor = TakeFirst()
	
class AgenciesSpider(CrawlSpider):
	name = "agencies"
	allowed_domains = ["lookbook.adage.com"]
	
	start_urls = ["http://lookbook.adage.com/", "http://lookbook.adage.com/Agencies/(offset)/"]		
	
	rules = (
			
		Rule(SgmlLinkExtractor(allow=('(\d*)', )), callback='parse_items', follow=True),
		Rule(SgmlLinkExtractor(allow=('lookbook\.adage\.com/[A-Z][a-zA-Z_/]+$', )), callback='parse_items', follow=True),
		
	)
	
	def parse_items(self, response):
		hxs = HtmlXPathSelector(response)
		agencies = hxs.select("//div[@class='editable']/div[@class='left']")
		items = []		
		
		for agency in agencies:
			loader = AgenciesLoader(selector=agency)
			loader.add_xpath('agency_name', "h1/text()")
			loader.add_xpath('address', "address/span[@class='address']/text()")
			loader.add_xpath('city', "address/span[@class='city']/text()")
			loader.add_xpath('state', "address/span[@class='state']/text()")
			loader.add_xpath('address_zip', "address/span[@class='zip']/text()")
			loader.add_xpath('phone', "div[@class='attribute-phone']/text()")
			loader.add_xpath('website', "div[@class='attribute-url']/a/@href")
			items.append(loader.load_item())
		return items

