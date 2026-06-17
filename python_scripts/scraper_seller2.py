# This script is used to scrape data from eBay product pages. It reads a list of URLs from a text file, retrieves the HTML content of each page, and extracts specific information such as the title, price, dimensions, inventory, material, fringe, knot count, and condition of the product.
# The extracted data is then saved to a CSV file for further analysis or use.
# Before running the script, ensure you have a text file containing the URLs of the eBay product pages you want to scrape.
# The script will prompt you to enter the location of this file if it cannot be found in the default directory.
# After running the script, the extracted data will be saved to a CSV file in the same directory.
# 
# Note: The script uses the BeautifulSoup library for parsing HTML and the colorama library for colored terminal output.
# Make sure to install these libraries if you haven't already. You can install them using pip:
# pip install beautifulsoup4 colorama

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as bs
import re
import os
import csv

from colorama import init, Fore
init(convert=True)

directory = os.path.dirname(os.path.realpath(__file__))
location = directory + "/extacted urls.txt"
while True:
    try:
        urltxt = open(location)
        break
    except:
        print(Fore.RED + "Couldn't find the file with given directory!" + Fore.WHITE)
        location = input("Enter the file directory: ").strip("\n\t\"\' ")
urls = urltxt.read().split("\n")
urltxt.close()

exportlocation = directory + "/data.csv"
exportfh = open(exportlocation, "w", newline="")
csvfh = csv.writer(exportfh)
specs = {"URL":"", "Title":"", "Price":"", "Length":"", "Width":"", "Inventory":"", "Art":"", "Pile":"", "Fringe":"", "Knot":"", "Status":""}
csvfh.writerow(specs.keys())


headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

authinfo = urllib.request.HTTPBasicAuthHandler()
opener = urllib.request.build_opener(authinfo, urllib.request.CacheFTPHandler)
urllib.request.install_opener(opener)

for url in urls:
    if len(url.strip()) < 1:
        continue
    print("Retriving:", url)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    page = response.read()
    soup = bs(page, "html.parser")

    # This site uses more universal class names and tags, so we can use more general selectors to extract the data.
    specs["URL"] = url
    try: specs["Title"] = soup.find("span", {"id":"vi-lkhdr-itmTitl"}).text.strip()
    except: specs["Title"] = "ERROR"
    try: specs["Price"] = soup.find("span", {"itemprop":"price"})["content"].strip()
    except: specs["Price"] = "ERROR"
    try: specs["Length"] = re.findall("\(?\s*?(\d+)\s*?x\s*?",specs["Title"], re.IGNORECASE)[0]
    except: specs["Length"] = "ERROR"
    try: specs["Width"] = re.findall("\s*?x\s*?(\d+)\)?",specs["Title"], re.IGNORECASE)[0]
    except: specs["Width"] = "ERROR"
    try: 
        specs["Inventory"] = re.findall("\d+", specs["Title"])
        specs["Inventory"].remove(specs["Length"])
        specs["Inventory"].remove(specs["Width"])
        specs["Inventory"] = specs["Inventory"][0]
    except: specs["Inventory"] = "ERROR"
    try: specs["Art"] = soup.find(text=re.compile(".*regionales\s*design:*", re.IGNORECASE)).parent.parent.parent.parent.next_sibling.text
    except: specs["Art"] = "ERROR"
    try: specs["Material"] = soup.find(text=re.compile(".*material:*", re.IGNORECASE)).parent.parent.parent.parent.next_sibling.text
    except: specs["Material"] = "ERROR"


    try: specs["Fringe"] = re.findall("Kette\s*?:([A-Za-zÄäÖöÜüßẞ0-9%,\s]+)\s+?[A-Za-zÄäÖöÜüßẞ]+\s*?:", desc, re.IGNORECASE)[0].strip()
    except: specs["Fringe"] = "ERROR"
    try: specs["Knot"] = re.findall("Knotenzahl\s*?:\s*?[A-Za-zÄäÖöÜüßẞ\.\s]*(\d+.?\d+)", desc, re.IGNORECASE)[0].strip().replace(".", "")
    except: specs["Knot"] = "ERROR"
    try: specs["Status"] = re.findall("Zustand\s*?:([A-Za-zÄäÖöÜüßẞ,\s]+)Geschätzter", desc, re.IGNORECASE)[0].strip()
    except: specs["Status"] = "ERROR"
    csvfh.writerow(specs.values())

print(f"Data from {len(urls)} products mined successfully!")
exportfh.close()
print(f"Data exported to {exportlocation}.")