# Run this on a copy of the dataset to convert each xml into xml.bz2
#find . -type f -exec bzip2 {} +

# Then run this on a particular category to get the concatenated bz2
bzip2 -dc *.bz2 | bzip2 > output.xml.bz2

# Wikiextractor
bzcat output.xml.bz2 |
  ../../../WikiExtractor.py -cb 250K -o extracted

find extracted -name '*bz2' -exec bunzip2 -c {} \; > text.xml
rm -rf extracted

# Remove all xml/html tags from a file
sed -n '/^$/!{s/<[^>]*>//g;p;}' text.xml > text.txt
