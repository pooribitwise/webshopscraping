# This script is used to generate a CSV file containing URLs of images based on the files present in the same directory. It looks for files that are JPEG images and have a specific naming pattern (starting with "F" followed by a number).
# The generated URLs are formatted to point to a specific location on a web server, and the output is saved in a CSV file named "data.csv".

# Note: The script assumes that the images are hosted on a web server with a specific URL structure. Make sure to replace "YOURDOMAIN" in the generated URLs with the actual domain where your images are hosted.

import os

directory = os.path.dirname(os.path.realpath(__file__))

lst = os.listdir(directory)

explocation = directory + "/data.csv"
exp = open(explocation, "w", newline="\n")

for num in range(1001, 1253):
    tmp= []
    for name in lst:
        if name.endswith(".jpg") and name.startswith(f"F{num}"):
            tmp.append("https://YOURDOMAIN/wp-content/uploads/" + name.replace(" (", "-").replace(")", ""))
    exp.write(','.join(tmp) + ';\n')
        
exp.close()
