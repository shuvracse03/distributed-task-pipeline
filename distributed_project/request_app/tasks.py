from celery import Celery
from celery import shared_task

#BROKER ='pyamqp://guest@localhost//'

BROKER='amqp://admin:pass123@localhost:5672/myvhost'

app = Celery('distributed_project', backend='rpc://', broker=BROKER)


@app.task
def scrape_books(book_types):
    print('inside scrape books')
    if ',' in book_types:
       splitted = book_types.split(',')
    else:
       splitted=[book_types]
    print(len(splitted))
    return book_types
