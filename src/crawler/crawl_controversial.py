import requests
import os
import errno
from BeautifulSoup import BeautifulSoup

def find_categories(tree):
    links = dict()
    for h in tree.findAll('h3'):
        titles = []
        category = h.findAll('span')[1].text
        if category == "":
            print "Caterogry is Empty"
        for l in h.findNextSibling().findAll('a'):
            titles.append(l.attrs[1][1])
        links[str(category)] = titles
    return links

def download_article(title):
    url = "http://en.wikipedia.org/w/api.php"
    payload = {'action': 'query', 'titles': title, 'format': 'json', 'export': 'exportnowrap'}
    r = requests.get(url, params = payload)
    return r.json['query']['export']['*']

def save_article_to_file(category, title, text):
    category = category.replace("/", "_")
    title = title.replace("/","_")
    directory = "../../dataset/controversial/" + category
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
    r = requests.get("http://en.wikipedia.org/wiki/Wikipedia:List_of_controversial_issues")
    soup = BeautifulSoup(r.text)
    links = find_categories(soup)
    for category in links.keys():
        for title in links[category]:
            text = download_article(title)
            save_article_to_file(category,title,text)
            print "Article %s in category %s has been saved" %(title,category)

def main():
    crawl()

if __name__ == "__main__":
    main()
