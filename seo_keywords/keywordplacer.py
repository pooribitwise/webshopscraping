# This script reads keywords from a merged text file and appends them to a CSV file in a specific format for wordpress bulk import.

import os
import csv

directory = os.path.dirname(os.path.realpath(__file__))

inp = open(os.path.join(directory, "merged.txt"), "r")
keywords = inp.read().split('\n')
inp.close()

# take an export from woocommerce and add the keywords to the end of each line, separated by a semicolon, in the format "keyword1||||keyword2||||keyword3"
csvin = open(os.path.join(directory, "csvs", "keywords.csv"), "r", encoding="utf-8-sig")
csvout = open(os.path.join(directory, "keywordsout.csv"), "w")

i = 0
l = 0
for line in csvin:
    if l == 0:
        csvout.write(line.strip() + '\n')
        l = 1
        continue
    csvout.write(line.strip() + ';' + '"' + str('||||'.join([keywords[j].strip() for j in range(i*11, 11*(i+1))])).strip() + '"' + '\n')
    i = i+1