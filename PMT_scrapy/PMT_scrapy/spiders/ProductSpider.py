import scrapy
from PMT_scrapy.PMT_scrapy.items import AmazonItem, FlipkartItem, SnapdealItem, EbayItem
import json
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

def urls_list(name):
  with open(r"PMT_scrapy\PMT_scrapy\spiders\url_list.json", 'r') as urls:
    dictionary = json.load(urls)
    urls.close()
  return dictionary[name]

class amazonspider(scrapy.Spider):
  name = "amazonspider"

  custom_settings = {
                        "FEEDS": {
                            "amazon_items.json": {"format": "json"},
                        },
                    }
  
  def start_requests(self):
    urls = urls_list('amazon_url')
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)
  
  def parse(self, response):
    items = AmazonItem()
    title = response.xpath('//*[@id="productTitle"]/text()').get()
    price = response.xpath('//*[@id="priceblock_ourprice"]/text()').get()
    if price is None:
      price = response.xpath('//*[@id="priceblock_dealprice"]/text()').get()
    avail = response.xpath('//*[@id="availability"]')
    if title and price and avail:
      price = price.replace(",","")
      sale_price = re.findall(r"\d+", price)
      availability = avail.css("span::text").get()
    
      items['product_name'] = ''.join(title).strip()
      items['product_sale_price'] = ''.join(sale_price[0]).strip()
      items['product_availability'] = ''.join(availability).strip()
      items['product_url'] = response.url
      
      yield items

class flipkartspider(scrapy.Spider):
  name = "flipkartspider"

  custom_settings = {
                        "FEEDS": {
                            "flipkart_items.json": {"format": "json"},
                        },
                    }

  def start_requests(self):
    urls = urls_list('flipkart_url')
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    items = FlipkartItem()
    title = response.xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()
    sale_price = response.selector.css('._1vC4OE::text').get()
    avail = response.xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[3]').get()
    if avail and title and sale_price:
      if 'Available' in avail:
        availability = "Available"
      else:
        availability = "Sold Out"
      sale_price = sale_price.replace(",","")
      sale_price = re.findall(r"\d+", sale_price)
      items['product_name'] = ''.join(title).strip()
      items['product_sale_price'] = ''.join(sale_price).strip()
      items['product_availability'] = ''.join(availability).strip()
      items['product_url'] = response.url
      yield items

class snapdealspider(scrapy.Spider):
  name = "snapdealspider"

  custom_settings = {
                        "FEEDS": {
                            "snapdeal_items.json": {"format": "json"},
                        },
                    }

  def start_requests(self):
    urls = urls_list('snapdeal_url')
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    items = SnapdealItem()
    title = response.xpath('/html/body/div[11]/section/div[1]/div[2]/div/div[1]/div[1]/div[1]/h1/text()').get()
    sale_price = response.selector.css('.payBlkBig::text').get()
    try:
      avail = response.xpath('.sold-out-err::text').get()
    except ValueError:
      avail = "Available"
    if avail and title and sale_price:
      sale_price = sale_price.replace(",","")
      sale_price = re.findall(r"\d+", sale_price)
      items['product_name'] = ''.join(title).strip()
      items['product_sale_price'] = ''.join(sale_price).strip()
      items['product_availability'] = ''.join(avail).strip()
      items['product_url'] = response.url
      yield items

class ebayspider(scrapy.Spider):
  name = "ebayspider"

  custom_settings = {
                        "FEEDS": {
                            "ebay_items.json": {"format": "json"},
                        },
                    }

  def start_requests(self):
    urls = urls_list('ebay_url')
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    items = EbayItem()
    title = response.css('[id="itemTitle"]::text').get()
    sale_price = response.css('[id="convbinPrice"]::text').get()
    avail = "Available"
    try:
      avail = response.css('[id="qtySubTxt"]').getall()[0]
      if 'available' in avail.lower():
        avail = "Available"
      else:
        avail = "Sold Out"
    except:
      pass
    
    if avail and title and sale_price:
      sale_price = sale_price.replace(",","")
      sale_price = sale_price.split()[1]
      sale_price = sale_price.split(".")[0]
      items['product_name'] = ''.join(title).strip()
      items['product_sale_price'] = ''.join(sale_price).strip()
      items['product_availability'] = ''.join(avail).strip()
      items['product_url'] = response.url
      yield items


def run_all_spiders():
  if os.path.exists("amazon_items.json"):
    os.remove("amazon_items.json")
  if os.path.exists("flipkart_items.json"):
    os.remove("flipkart_items.json")
  if os.path.exists("snapdeal_items.json"):
    os.remove("snapdeal_items.json")
  if os.path.exists("ebay_items.json"):
    os.remove("ebay_items.json")
  process = CrawlerProcess(get_project_settings())
  process.crawl(amazonspider)
  process.crawl(flipkartspider)
  process.crawl(snapdealspider)
  process.crawl(ebayspider)
  process.start()