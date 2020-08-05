from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Price_Monitoring_Tool.Price_Monitoring_Tool.spiders import ProductSpider
from Display import pprint
import json               
  
import time 

def match_keyword_in_url(url, keywords):
	for keyword in keywords:
		if keyword not in url:
			return False
	return True

def update_urldata(url_list, item_to_search, url_name):
	final_list = []
	with open(r"Price_Monitoring_Tool\Price_Monitoring_Tool\spiders\url_list.json", "r") as oldfile:
		dictionary = json.load(oldfile)
		oldfile.close()

	item_to_search = item_to_search.lower().split()

	for url in url_list:
		if match_keyword_in_url(url, item_to_search):
			final_list.append(url)

	dictionary[url_name] = list(set(final_list))
	json_object = json.dumps(dictionary, indent=4)

	with open(r"Price_Monitoring_Tool\Price_Monitoring_Tool\spiders\url_list.json", "w") as output:
		output.write(json_object)
		output.close()

def get_minimum():
	product_details = []
	files = ["amazon_items.json", "flipkart_items.json", "snapdeal_items.json"]
	for file in files:
		with open(file, "r") as details:
			content = json.load(details)
			product_details.append(content)
			details.close()
	amazon = sorted(product_details[0], key = lambda x: x["product_sale_price"])
	amazon = amazon[:3]
	flipkart = sorted(product_details[1], key = lambda x: x["product_sale_price"])
	flipkart = flipkart[:3]
	snapdeal = sorted(product_details[2], key = lambda x: x["product_sale_price"])
	snapdeal = snapdeal[:3]
	return pprint(min([amazon[0], flipkart[0], snapdeal[0]], key = lambda x:x['product_sale_price']))


def amazon_scrape(URL, item_to_search):        
	browser = webdriver.Firefox(executable_path="geckodriver.exe")
	browser.get(URL)
	try: 
		element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))) 
	except TimeoutException as e: 
	    print("Time out!")
	    return
    

	browser.find_element_by_id('twotabsearchtextbox').send_keys(item_to_search + Keys.RETURN)
	
	try:
		results = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sg-col-inner")))[3]
	except TimeoutException as e:
		print("Time out!")	

	url_list = []

	time.sleep(2)
	
	if results:
		for result in results.find_elements_by_tag_name('a'):
			url_list.append(result.get_attribute("href"))

		update_urldata(url_list, item_to_search, "amazon_url")

		return (print("GOT URLs FROM AMAZON\n"))

def flipkart_scrape(URL, item_to_search):
	browser = webdriver.Firefox(executable_path="geckodriver.exe")
	browser.get(URL)

	try:
		element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'LM6RPg')))
	except TimeoutException as e:
		print("Time out!")
		return

	browser.find_element_by_class_name('LM6RPg').send_keys(item_to_search + Keys.RETURN)

	try:
		results1 = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1HmYoV:nth-child(2)")))
		results2 = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._3e7xtJ > div:nth-child(1) > div:nth-child(2)")))
	except TimeoutException as e:
		print("Time out!")

	url_list = []

	time.sleep(2)

	if results1:
		for result in results1.find_elements_by_tag_name('a'):
			url_list.append(result.get_attribute("href"))

	if results2:
		for result in results2.find_elements_by_tag_name('a'):
			url_list.append(result.get_attribute("href"))

		update_urldata(url_list, item_to_search, "flipkart_url")

		return (print("GOT URLs FROM FLIPKART\n"))


def snapdeal_scrape(URL, item_to_search):
	browser = webdriver.Firefox(executable_path="geckodriver.exe")
	browser.get(URL)

	try:
		element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'inputValEnter')))
	except TimeoutException as e:
		print("Time out!")
		return

	browser.find_element_by_id('inputValEnter').send_keys(item_to_search + Keys.RETURN)

	try:
		results = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#products")))
	except TimeoutException as e:
		print("Time out!")

	url_list = []

	time.sleep(2)

	if results:
		for result in results.find_elements_by_tag_name('a'):
			url_list.append(result.get_attribute("href"))

		update_urldata(url_list, item_to_search, "snapdeal_url")

		return (print("GOT URLs FROM SNAPDEAL\n"))

def tatacliq_scrape(URL, item_to_search):
	browser = webdriver.Firefox(executable_path="geckodriver.exe")
	browser.get(URL)

	try:
		element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_2wBdAJ6BFwpXejbzsJBPO0')))
	except TimeoutException as e:
		print("Time out!")

	browser.find_element_by_class_name('_2wBdAJ6BFwpXejbzsJBPO0').send_keys(item_to_search + Keys.RETURN)

	try:
		results = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "grid-container")))
	except TimeoutException as e:
		print("Time out!")

	url_list = []

	time.sleep(2)

	if results:
		for result in results.find_elements_by_tag_name('a'):
			url_list.append(result.get_attribute("href"))

		update_urldata(url_list, item_to_search, "tatacliq_url")

		return (print("GOT URLs FROM TATACLIQ\n"))


if __name__ == '__main__':
	item_to_search = input("Enter name of item: ")
	
	URL = 'https://www.amazon.in/'
	amazon_scrape(URL, item_to_search)

	URL = 'https://www.flipkart.com/'
	flipkart_scrape(URL, item_to_search)

	URL = 'https://www.snapdeal.com/'
	snapdeal_scrape(URL, item_to_search)

	URL = 'https://www.tatacliq.com/'
	tatacliq_scrape(URL, item_to_search)

	ProductSpider.run_all_spiders()

	get_minimum()
