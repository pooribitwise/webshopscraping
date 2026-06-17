# This script is used to organize image files based on a CSV file that contains key values and their corresponding categories.
# The script reads the CSV file, extracts the key values and categories, and then copies the image files (named after the key values) into their respective category folders. If an image file is missing, it will print the name of the missing file to the console.

import os
import csv
import shutil

directory = os.path.dirname(os.path.realpath(__file__))
csvloc = os.path.join(directory, "keyvalues.csv")

csvfh = open(csvloc, 'r')
csv_reader = csv.reader(csvfh, delimiter=';')

i=0
errors = list()
for row in csv_reader:
    if(i==0):
        i = 1
        continue
    lux = row[0]
    categories = row[1].split(',')
    for category in categories:
        try: shutil.copy(os.path.join(directory, f"{lux}.jpg"), os.path.join(os.path.join(directory, category), f"{lux}.jpg"))
        except: print(lux)