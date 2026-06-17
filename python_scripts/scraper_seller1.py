# This script is used to scrape data from the website of a german carpet seller.
# It extracts the price, inventory, length, width, flor, kette, knots, status and art of the carpets and exports it to a csv file.
# before running the script, make sure to have a text file with the urls of the products you want to scrape.
# run URL Extractor.py to extract the urls from the website and save them in a text file, then run this script to scrape the data and export it to a csv file.

# Note: The script uses the BeautifulSoup library for parsing HTML and the colorama library for colored terminal output.
# Make sure to install these libraries if you haven't already. You can install them using pip:
# pip install beautifulsoup4

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as bs
import re
import os
import csv


# load urls from text file, if the file is not found, ask the user to input the location of the file until a valid file is found
directory = os.path.dirname(os.path.realpath(__file__))
location = directory + "/extracted urls.txt"
while True:
    try:
        urltxt = open(location)
        break
    except:
        print("Couldn't find the file with given location!")
        location = input("Enter the file locaton: ").strip("\n\t\"\' ")
urls = urltxt.read().split("\n")
urltxt.close()

# create a csv file to export the data
exportlocation = directory + "/data.csv"
exportfh = open(exportlocation, "w", newline="")
csvfh = csv.writer(exportfh, delimiter=";")
# specs is a dictionary that will hold the data for each product.
specs = {"url":"", "price":"", "length":"", "width":"", "inventory":"", "flor":"", "kette":"", "knots":"", "status":"", "art":"", "images":[]}
csvfh.writerow(specs.keys())

# add headers to the request to avoid getting blocked by the website, and set up an opener to handle authentication and proxies if needed.
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
authinfo = urllib.request.HTTPBasicAuthHandler()

# to use proxy change commented lines
#proxy = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}
#proxy_support = urllib.request.ProxyHandler(proxy)
#opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)

opener = urllib.request.build_opener(authinfo, urllib.request.CacheFTPHandler)



urllib.request.install_opener(opener)

done = 0

for url in urls:
    if len(url.strip()) < 1:
        continue
    print("Retriving:", url, "-", f"{len(urls) - done - 1} Remaining...")
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    page = response.read()
    soup = bs(page, "html.parser")

    specs["url"] = url
    try: specs["price"] = soup.find("span", {"itemprop":"price"})["content"].strip()
    except: specs["price"] = "ERROR"
    try: specs["images"] = [image.img["src"].replace("s-l64", "s-l2000") for image in soup.find_all("button", {"class":"ux-image-filmstrip-carousel-item"})]
    except: specs["images"] = "ERROR"

    # the shop was using an iframe to display the description, so we need to extract the url of the iframe and make a new request to get the description.
    frame_url = soup.find("iframe", {"id":"desc_ifr"})["src"]
    print("Retriving:", frame_url)
    request = urllib.request.Request(frame_url, headers=headers)
    response = urllib.request.urlopen(request)
    page = response.read()
    soup = bs(page, "html.parser")

    description = soup.find_all("p")
    description = [tag.text for tag in description if not tag.text is None]
    description = [tag.strip() for tag in description if not len(tag.strip()) < 1]
    description = " ".join(description).replace("\xa0", " ")
    
    # use regular expressions to extract the data from the description, if the data is not found, set it to "ERROR".
    try: specs["art"] = re.findall("([A-Za-z1-9ÄäÖöÜüßẞ\/\s]+)\s+?[A-Za-zÄäÖöÜüßẞ]+\s+?Nr[\.\s:]*?", description, re.IGNORECASE)[0].strip().split()[0].split("/")[0].strip().capitalize()
    except: specs["art"] = "ERROR"
    try: specs["inventory"] = re.findall("Nr[\.\s:]*?(\d+)", description, re.IGNORECASE)[0].strip()
    except: specs["inventory"] = "ERROR"
    try: specs["length"] = re.findall("(\d{2,3})\s*?x\s*?\d{2,3}", description, re.IGNORECASE)[0].strip()
    except: specs["length"] = "ERROR"
    try: specs["width"] = re.findall("\d{2,3}\s*?x\s*?(\d{2,3})", description, re.IGNORECASE)[0].strip()
    except: specs["width"] = "ERROR"
    try: specs["flor"] = re.findall("Flor\s*?:([A-Za-zÄäÖöÜüßẞ0-9%&,\s\(\)\.]+)\s+?[A-Za-zÄäÖöÜüßẞ]+\s*?:", description, re.IGNORECASE)[0].strip()
    except: specs["flor"] = "ERROR"
    try: specs["kette"] = re.findall("Kette\s*?:([A-Za-zÄäÖöÜüßẞ0-9%&,\s]+)\s+?[()A-Za-zÄäÖöÜüßẞ]+\s*?", description, re.IGNORECASE)[0].strip()
    except: specs["kette"] = "ERROR"
    try: specs["knots"] = re.findall("Knotenzahl[A-Za-zÄäÖöÜüßẞ\s]*?:\s*?[()A-Za-zÄäÖöÜüßẞ\.\s]*(\d+.?\d+)", description, re.IGNORECASE)[0].replace(".", "").strip()
    except: specs["knots"] = "ERROR"
    try: specs["status"] = re.sub("flor", "", re.findall("artikel\szustand\s*?:([()A-Za-zÄäÖöÜüßẞ,\s]+).*?:", description, re.IGNORECASE)[0], flags=re.IGNORECASE).strip()
    except: specs["status"] = "ERROR"
    csvfh.writerow(specs.values())
    done = done + 1
print(f"Data from {len(urls)} products mined successfully!")
exportfh.close()
print(f"Data exported to {exportlocation}")
input("Press Enter to Exit...")