import os

folder1="../dataset/controversial/Politics_ Economics/"
folder2="../dataset/non-controversial/Politics/"

common = set(os.listdir(folder1)).intersection(set(os.listdir(folder2)))

for fileName in common:
    f = folder2+fileName
    os.remove(f)
    print "Removing : "+f
