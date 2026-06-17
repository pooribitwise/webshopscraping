# This script merges all keywords from the files in the directory into a single file called "merged.txt".
# Back then I was using windows and I didn't know cat exists.

import os

directory = os.path.dirname(os.path.realpath(__file__))

names = os.listdir(directory)
names.remove("merger.py")

keywords = []
for name in names:
    inp = open(os.path.join(directory, name), "r", encoding="utf-8")
    for line in inp:
        if not line.title() in keywords:
            keywords.append(line.title())
    inp.close()

out = open(os.path.join(directory, "merged.txt"), "w")
for keyword in keywords:
    out.write(keyword.strip() + '\n')
out.close()