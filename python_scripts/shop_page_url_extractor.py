# This script is used to extract all product urls from a search result on ebay.de and save them in a text file.
# It uses the BeautifulSoup library to parse the HTML of the search results and extract the relevant information.
# The script also handles pagination to ensure that all product URLs are collected from multiple pages of search results.
#
# Note: The script includes commented-out code for using a proxy, which can be useful for web scraping to avoid IP blocking.
# However, the proxy settings are currently disabled in the script.
# Make sure to install the BeautifulSoup library (bs4) before running this script, as it is required for parsing the HTML content.

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as bs
import re

import os

directory = os.path.dirname(os.path.realpath(__file__))
location = directory + r"/extracted urls.txt"
fh = open(location, "w")
SHOP_NAME = "YOUR_SCRAPING_SHOP_NAME"
url = f"https://www.ebay.de/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn={SHOP_NAME}&store_cat=0&store_name={SHOP_NAME}&_oac=1&_ipg=240"
urls = []
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)" }

authinfo = urllib.request.HTTPBasicAuthHandler()


#proxy = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}
#proxy_support = urllib.request.ProxyHandler(proxy)
#opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)

opener = urllib.request.build_opener(authinfo, urllib.request.CacheFTPHandler)


urllib.request.install_opener(opener)

while True:
    print("Retriving:", url)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    page = response.read()
    soup = bs(page, "html.parser")
    products = soup.findAll("div", {"class":"s-item__info clearfix"})
    for product in products:
        anchor = product.find("a", {"class":"s-item__link", "href":re.compile("https://www\.ebay\.de/itm/.+")})
        if not anchor is None:
            price = int(re.findall("EUR\s([0-9.]+),\d{2}?", product.find("span", {"class":"s-item__price"}).text)[0].replace(".", ""))
            title = product.find("div", {"class":"s-item__title"}).text
            if True:
                urls.append(anchor["href"])
    url = soup.find("a", {"class":"pagination__next icon-link"})
    if url is None:
        break
    url = url["href"]

print(f"{len(urls)} urls extracted.\nSaving...")
for link in urls:
    fh.write(link + "\n")
fh.close()
print(f"File Saved Successfully in {location}")
print(f"Now you can run scraper_seller.py to extract the product information from the urls.")