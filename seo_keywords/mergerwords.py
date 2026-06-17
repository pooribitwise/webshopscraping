# This script merges all keywords from the files in the directory into a single file called "merged.txt".
# Back then I was using windows and I didn't know cat exists.

import os

directory = os.path.dirname(os.path.realpath(__file__))

names = os.listdir(directory)
names.remove("merger.py")

keywords = []
for name in names:
    inp = open(os.path.join(directory, name), 'r')
    for line in inp:
        words = line.title().split(" ")
        for word in words:
            if not word in keywords:
                keywords.append(word)
    inp.close()

out = open(os.path.join(directory, "merged.txt"), 'w')
for keyword in keywords:
    out.write(keyword.strip() + '\n')
out.close()