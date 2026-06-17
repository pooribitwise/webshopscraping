# This script is used to download images from eBay product pages.
# It reads a CSV file containing product names and their corresponding image URLs, and then downloads each image to a specified directory.
# Before running the script, ensure you have a CSV file with the product names in the first column and a list of image URLs in the second column (formatted as a Python list).
# The script will save the images in the same directory as the script, with filenames based on the product names and an index for multiple images of the same product.
#
# Note: The script uses the requests library for downloading images. Make sure to install this library if you haven't already. You can install it using pip:
# pip install requests

import os, csv, requests, shutil

directory = os.path.dirname(os.path.realpath(__file__))
csvloc = directory + r"/image_urls.csv"

csvfh = open(csvloc, 'r')
csv_reader = csv.reader(csvfh, delimiter=';')

for row in csv_reader:
    lux = row[0]
    imgurls = eval(row[1])
    i = 1
    for imgurl in imgurls:
        file_name = directory+f"/{lux} ({i}).jpg"
        res = requests.get(imgurl, stream = True)
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Sucessfully Downloaded: ', file_name)
        else:
            print('Couldn\'t be retrieved', file_name)
        i += 1