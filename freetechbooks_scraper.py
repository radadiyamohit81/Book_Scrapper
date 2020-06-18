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

main_url = 'http://www.freetechbooks.com/topics'
r = requests.get(main_url, headers=headers)
page = 1

print('Start scraping {}'.format(main_url))

while page < 82:
    bsObj = BeautifulSoup(r.content, 'html.parser')
    links_per_page = bsObj.findAll('p', {'class': 'media-heading lead'})
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
            download_link = newbsObj.find('div', {'id': 'srvata-content'}).a['href']
            print(download_link)
        except:
            download_link = 'no download link found'
        try:
            author_data = newbsObj.findAll('div', {'class': 'media-body'})[1].findAll('a')
            for data in author_data:
                if data.find('i', 'fa-user'):
                    author = data.get_text().lstrip()
                    print(author)
        except:
            author = 'not found'

        # File size is not available here.
        size = 'not found'

        # Category is not available here.
        category = 'not found'

        try:
            date_paragraph = newbsObj.find(string= 'Publication date').parent.parent
            date_list = list(date_paragraph)
            date = str(date_list[1].strip(': '))
            print(date)
        except:
            date = 'not found'

        ##############################
        # Place the book_obj code here
        ##############################

    print('---------------------------------------------------------------')
    next_page = main_url + '?page=' + str(page)
    print(next_page)
    page +=1
    r = requests.get(next_page, headers=headers)


print('---------------------------------------------------------------')
print('{} compeletely scraped.'.format(main_url))
print('---------------------------------------------------------------')
