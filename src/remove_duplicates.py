import os
folder="/home/pankajm/Downloads/datas/"
folder1= folder+"Politics/non-controversial/"
folder2= folder+"Economics/non-controversial/"

common = set(os.listdir(folder1)).intersection(set(os.listdir(folder2)))

for fileName in common:
    f = folder2+fileName
    os.remove(f)
    print "Removing : "+f
