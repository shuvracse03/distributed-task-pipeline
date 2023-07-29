from celery import Celery
from celery import shared_task
from bs4 import BeautifulSoup
import requests
import re
import json
from celery import group

from request_app.models import *
#BROKER ='pyamqp://guest@localhost//'

BROKER='amqp://admin:pass123@localhost:5672/myvhost'

app = Celery('distributed_project', backend='rpc://', broker=BROKER)

def get_links_from_pages(page_no,url):
    if page_no !=1:
       clean_url = url.rsplit('/',1)[0] + '/'+ f'page-{page_no}.html'
    else:
       clean_url = url
    #https://books.toscrape.com/catalogue/category/books/fiction_10/page-2.html
  
    r= requests.get(clean_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    h3s= soup.find_all('h3')
    links = []
    BASE_URL = 'https://books.toscrape.com/catalogue/'
    for h3 in h3s:
        try:
          
          product_link = h3.find('a').attrs.get('href','')
          split_link = product_link.split('/')
          clean_link = BASE_URL+split_link[-2]+'/'+split_link[-1]
          links.append(clean_link)
        except:
           pass
    return links
   
def insert_to_db(json_list):
   product_list = []
   for elem in json_list:
       product_list.append(Product(title=elem['title'], parent_url = elem['parent_url'], description=elem['description'],\
       upc=elem['upc'], product_type=elem['product_type'], price_exclude_tax=elem['price_exclude_tax'],\
        price_include_tax=elem['price_include_tax'], currency=elem['currency'], tax=elem['tax'], stock=elem['stock'], no_reviews=elem['no_reviews']))
   Product.objects.bulk_create(product_list) #Bulk insert
    
def get_product_links(url):
    
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    try:
       no_pages = int(soup.find('li', {"class": "current"}).text.strip().split(' ')[-1])
    except:
       no_pages =1
    all_links=[]
    for page_no in range(1,no_pages+1):
       links = get_links_from_pages(page_no, url)
       all_links = all_links + links
       
    return all_links
    
def get_book_info(url, parent_url):
    info={}
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    product_main = soup.find('div', {"class": "col-sm-6 product_main"})
    info['title'] = soup.find('h1').text
    info['description'] =  soup.find('div', {"id": "product_description"}).find_next_sibling("p").text
    data ={}
    
    rows = soup.find_all('tr')
 
    for row in rows:
       th = row.find('th').text.strip()
       td = row.find('td').text.strip()
       data[th] = td
 
    info['upc'] = data['UPC']
    info['no_reviews'] = int(data['Number of reviews'])
    info['product_type'] = data['Product Type']
    info['price_exclude_tax'] = re.sub("[^\d\.]", "", data['Price (excl. tax)'])
    info['price_include_tax'] = re.sub("[^\d\.]", "", data['Price (incl. tax)'])
    info['tax'] = re.sub("[^\d\.]", "", data['Tax'])
    
    try:
      info['stock'] = int(data['Availability'].split('(')[1].split(' ')[0])
    except:
       info['stock'] = 0
    currency = ''
    for char in data['Tax']:
       if char.isalpha():
          currency+=char
    info['currency'] = currency
    info['parent_url'] = parent_url
    return info
    
def get_all_infos(links, parent_url):
    result_list = []
    for a_link in links:
        result= get_book_info(a_link, parent_url)
        result_list.append(result)
    return result_list
    
def get_book_categories():
   url ='https://books.toscrape.com/catalogue/category/books_1/index.html'
   r = requests.get(url)
   soup = BeautifulSoup(r.text, 'html.parser')
   side_categories = soup.find('div', {"class": "side_categories"})
   category_links = side_categories.find_all('a')
   link_json={}
   BASE_URL ='https://books.toscrape.com/catalogue/category/'
   for a_link in category_links:
       if a_link.text.strip()=='Books':
          continue
       url = a_link.attrs.get('href','')
       splitted = url.split('/',1)[1]
       url = BASE_URL + splitted
       link_json[a_link.text.strip()] =url
   return link_json
   
@app.task
def process_link(url):
    links = get_product_links(url) # get all product links from category url
    all_infos = get_all_infos(links, url) # now get information from each product link
    insert_to_db(all_infos) # insert to database

@app.task
def scrape_books(user_selection):
    
    book_cats = get_book_categories()
    #select all book category links
    if user_selection.lower() =='all' or user_selection is None:
       chosen_cats = list(book_cats.values())
    else:
       #Choosing the links of the user selected categories
       chosen_cats=[]
       user_selections=user_selection.split(',')
       for elem in user_selections:
           if book_cats.get(elem.strip(),'')!='':
               chosen_cats.append(book_cats[elem])

    jobs = group(process_link.s(item) for item in chosen_cats)#A group is used to execute several tasks in parallel.
    jobs.apply_async()

    return chosen_cats
