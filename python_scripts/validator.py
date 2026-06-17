# This script is used to validate a list of URLs by checking if they are accessible and if they contain specific text indicating that the offer has ended or that the page was not found. The script reads URLs from a text file, makes HTTP requests to each URL, and categorizes them as valid, ended, or invalid based on the response.
# The results are printed to the console and saved to a new text file for any invalid or ended URLs.
#
# This was used to check if the products are still available on ebay.de before running the scraper to extract product information.
#
# Note: install the colorama library before running this script, as it is used for colored console output. You can install it using pip:
# pip install colorama

import urllib.request, urllib.parse, urllib.error

from colorama import init, Fore
init(convert=True)

import os

directory = os.path.dirname(os.path.realpath(__file__))

while True:
    try:
        urltxt = open(directory + "/urls.txt")
        break
    except:
        print(Fore.RED + "Couldn't find the file with given directory!" + Fore.WHITE)
        directory = input("Enter directory: ").strip("\n\t\"\'\\ ")

urls = urltxt.read()
urltxt.close()
urls = urls.split("\n")
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
authinfo = urllib.request.HTTPBasicAuthHandler()

# For using proxy uncomment the lines below
# proxy = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}
# proxy_support = urllib.request.ProxyHandler(proxy)
# opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)
opener = urllib.request.build_opener(authinfo, urllib.request.CacheFTPHandler)

urllib.request.install_opener(opener)

ended = []
invalid = []

text = bytes("Dieses Angebot wurde beendet.", "utf-8")
error = bytes("Wir haben überall gesucht.", "utf-8")

length = len(urls)
print(f"Validating {length} url(s)... ")
done = 0
for url in urls:
    url = url.strip("\t\n ,")
    if not url:
        continue
    print("Validating: " + url + " - ", end="")
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        page = response.read()
    except:
        print(Fore.RED + "invalid!" + Fore.WHITE)
        invalid.append(url)
        continue
    if error in page:
        print(Fore.RED + "not found!" + Fore.WHITE)
        invalid.append(url)
        continue
    if text in page:
        ended.append(url)
        print(Fore.YELLOW + "ended", end="")
    else:
        print(Fore.GREEN + "valid", end = "")
    done += 1
    print(Fore.WHITE + f" - {done} Done {length - done} Remaining.")

if len(invalid)>0 or len(ended)>0:
    exp = open(directory + "/invalid urls.txt", "w")

if len(invalid)>0:
    print("\nThe url(s) below are invalid or not found:" + Fore.RED)
    for url in invalid:
        print(url)
        exp.write(url + "\n")

if len(ended)>0:
    print(Fore.WHITE + "\nThe url(s) below are ended:")
    for url in ended:
        print(Fore.YELLOW + url)
        exp.write(url + "\n")

print(Fore.GREEN + f"\n{done} url(s) validated and {len(ended)} url(s) was ended." + Fore.WHITE)
try:
    exp.close()
    print("File saved successfully")
except:
    pass

input("Press Enter to continue...")