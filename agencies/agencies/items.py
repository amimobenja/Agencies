from scrapy.item import Item, Field

class AgenciesItem(Item):
	agency_name = Field()
	address = Field()
	city = Field()
	state = Field()
	address_zip = Field()
	phone = Field()
	website = Field()
