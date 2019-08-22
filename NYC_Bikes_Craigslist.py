#### view current path

# import os
#
# dirpath = os.getcwd()
# print("current directory is : " + dirpath)
# foldername = os.path.basename(dirpath)
# print("Directory name is : " + foldername)


#### https://www.youtube.com/watch?v=4o2Eas2WqAQ
#### API pull in python

## import packages
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import urllib.request
import lxml
from bs4 import BeautifulSoup

binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

class CraigslistScraper(object):
    def __init__(self, location, postal, min_price, max_price, radius, sort):
        self.location = location  # newyork
        self.postal = postal
        self.min_price = min_price
        self.max_price = max_price
        self.radius = radius
        self.sort = sort  # date, dist, priceasc, pricedsc

        # https://newyork.craigslist.org/search/bia?sort=priceasc&search_distance=3&postal=11222&min_price=100&max_price=300

        self.url = f"https://{location}.craigslist.org/search/bia?sort={sort}&search_distance={radius}&postal={postal}" \
            f"&min_price={min_price}&max_price={max_price}"

        self.driver = webdriver.Firefox(firefox_binary=binary)
        self.delay = 20

    # prints url
    # def test(self):
    #     print(self.url)

    def load_craigslist_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("page is ready")
        except TimeoutException:
            print("Up delay time")

    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name("result-row")

        dates = []
        titles = []
        prices = []

        for post in all_posts:
            title = post.text.split("$")

            if title[0] == '':
                title = title[1]
            else:
                title = title[0]

            title = title.split("\n")
            price = title[0]
            title = title[-1]

            title = title.split(" ")

            month = title[0]
            day = title[1]
            title = ' '.join(title[2:])
            date = month + " " + day

            print("PRICE: " + price)  # toggle
            print("TITLE: " + title)  # toggle
            print("DATE: " + date)    # toggle

            titles.append(title)
            prices.append(price)
            dates.append(date)
        return titles, prices, dates

    def extract_post_urls(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll("a", {"class": "result-title hdrlnk"}):
            print(link["href"])
            url_list.append(link["href"])
        return url_list

    def quit(self):
        self.driver.close()

location = "newyork"
postal = "11222"
min_price = "100"
max_price = "300"
radius = "3"
sort = "date"

scraper = CraigslistScraper(location, postal, min_price, max_price, radius, sort)
scraper.load_craigslist_url()
titles, prices, dates = scraper.extract_post_information()
scraper.extract_post_information()
# print(titles)     turn on for list
#scraper.extract_post_urls()     turn on for URLs
scraper.quit()