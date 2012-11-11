import sys
from BeautifulSoup import BeautifulSoup

f = open(sys.argv[1])
s = f.read()
soup = BeautifulSoup(s)

g = open(sys.argv[1]+".txt",'w')
for doc in soup.findAll('doc'):
    g.write(doc.text.encode('utf-8'))

g.close()
f.close()

