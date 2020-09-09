# -*- coding: utf-8 -*-
 
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
 
import scrapy
 
class AmazonItem(scrapy.Item):
  product_name = scrapy.Field()
  product_sale_price = scrapy.Field()
  product_availability = scrapy.Field()
  product_url = scrapy.Field()

class FlipkartItem(scrapy.Item):
  product_name = scrapy.Field()
  product_sale_price = scrapy.Field()
  product_availability = scrapy.Field()
  product_url = scrapy.Field()

class SnapdealItem(scrapy.Item):
  product_name = scrapy.Field()
  product_sale_price = scrapy.Field()
  product_availability = scrapy.Field()
  product_url = scrapy.Field()

class EbayItem(scrapy.Item):
  product_name = scrapy.Field()
  product_sale_price = scrapy.Field()
  product_availability = scrapy.Field()
  product_url = scrapy.Field()