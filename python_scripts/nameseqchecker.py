# This script is used to check for missing image files in a sequence. It looks for files that follow a specific naming pattern (e.g., "F1001 (1).jpg", "F1001 (2).jpg", etc.) and identifies any missing files in the sequence. The script will print the names of the missing files to the console.

import os, re

directory = os.path.dirname(os.path.realpath(__file__))

lst = os.listdir(directory)

for num in range(1001, 1253):
    i = 1
    while True:
        if not f"F{num} ({i}).jpg" in lst:
            if f"F{num} ({i+1}).jpg" in lst:
                print(f"F{num} ({i}).jpg")
            i = 1
            break
        i += 1
