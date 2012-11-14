import os
folder="/home/pankajm/prog/Vivaad/data/Politics_ Economics/"
folder1= folder+"controversial/"
folder2= folder+"non-controversial/"

common = set(os.listdir(folder1)).intersection(set(os.listdir(folder2)))

for fileName in common:
    f = folder2+fileName
    os.remove(f)
    print "Removing : "+f
