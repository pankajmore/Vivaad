import requests
import os
import errno
import time
from BeautifulSoup import BeautifulSoup

def find_pages(tree):
    titles = []
    for h in tree.findAll('h2'):
        for l in h.findNextSibling().findAll('a'):
            try:
                t = l.attrs[1][1]
                titles.append(t)
            except:
                print "Out of range"
            
    return titles

def download_article(title,category):
    url = "http://en.wikipedia.org/w/api.php"
    payload = {'action': 'query', 'titles': title, 'format': 'json', 'export': 'exportnowrap', 'redirects' : 'true' }
    try:
        r = requests.get(url, params = payload)
        save_article_to_file(category, title, r.json['query']['export']['*'])
    except requests.exceptions.ConnectionError:
        print "Connection Refused... Retrying in 5 seconds"
        time.sleep(5)
        download_article(title,category)

def save_article_to_file(category, title, text):
    category = category.replace("/", "_")
    title = title.replace("/","_")
    directory = "../../dataset/" + category + "/non-controversial/"
    make_sure_path_exists(directory)
    f = open(directory + "/"  + title + ".xml", 'w')
    f.write(text.encode('utf8'))
    f.close()

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def crawl():
    category = "Religion"
    url = "http://en.wikipedia.org/wiki/Index_of_religion-related_articles"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    titles = find_pages(soup)
    for title in titles:
        if title.startswith("Talk:"): # for a bug in religious cateogry
            pass
        download_article(title, category)
        print "Article %s in category %s has been saved" %(title,category)

def main():
    crawl()

if __name__ == "__main__":
    main()
