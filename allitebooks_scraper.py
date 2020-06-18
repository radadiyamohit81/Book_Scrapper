"""
Save the scraped data in hypercube's Book model in respective fields. i.e

from scraper.models import Book

book_obj = Book.objects.create(
                title=book_title,
                author=author,
                size=size,
                download_link=download_link,
                category=category,
                date=date
           )
"""

import requests
from bs4 import BeautifulSoup

mozilla_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
headers = {'User-Agent': mozilla_agent}

main_url = 'http://allitebooks.com'
r = requests.get(main_url, headers=headers)
page = 1

print('Start scraping {}'.format(main_url))

while page < 746:
    bsObj = BeautifulSoup(r.content, 'html.parser')
    links_per_page = bsObj.findAll('h2', {'class': 'entry-title'})
    for link in links_per_page:
        link_page = requests.get(link.a['href'], headers=headers)
        print('---------------------------------------------------------------')
        try:
            book_title = link.a.get_text()
            print(book_title)
        except:
            book_title = 'not found'
        newbsObj = BeautifulSoup(link_page.content, 'html.parser')
        try:
            download_link = newbsObj.find('span', {'class': 'download-links'}).a['href']
            print(download_link)
        except:
            download_link = 'no download link found'
        try:
            author = newbsObj.find('div', {'class': 'book-detail'}).dl.findAll('dd')[0].a.get_text()
            print(author)
        except:
            author = 'not found'
        try:
            size = newbsObj.find('div', {'class': 'book-detail'}).dl.findAll('dd')[5].get_text()
            print(size)
        except:
            size = 'not found'
        try:
            category = newbsObj.find('div', {'class': 'book-detail'}).dl.findAll('dd')[7].a.get_text()
            print(category)
        except:
            category = 'Technology'
        try:
            date = newbsObj.find('div', {'class': 'book-detail'}).dl.findAll('dd')[2].get_text()
            print(date)
        except:
            date = 'not found'

        ##############################
        # Place the book_obj code here
        ##############################

    print('---------------------------------------------------------------')
    next_page = main_url + '/page/' + str(page)
    print(next_page)
    page +=1
    r = requests.get(next_page, headers=headers)


print('---------------------------------------------------------------')
print('{} compeletely scraped.'.format(main_url))
print('---------------------------------------------------------------')
