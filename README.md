# Project short description
The project runs a whole ETL pipeline using Celery, RabbitMQ, Docker. PyTest was used testing. AppMap used for profiling.
The task is to scrape data from https://books.toscrape.com/. User can select one/more categories to be scraped.

## How to run the project?
  docker-compose build <br>
  docker-compose up <br>
  
  From terminal: <br>
  curl -d '{"book_types":"Travel,Mystery,Historical Fiction"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/scrape_site/ <br>
  curl -d '{"book_types":"all"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/scrape_site/ <br>
  You will immediatly see some API response, and the scraping will start in the background. It takes some time to finish the tasks. <br>
  You can check the scraped data in: <br>
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'admin',
        'PASSWORD': 'pass123',
        'HOST': 'db',
        'PORT':5432
    }
}
  
  
## Workflow:
 After the user specifies the categories to scrape, they are validated first. After that, corresponding links of the
 categories are listed. This list of the links are distributed among the processes parallely[see tasks.py, scrape_books function].
 I used "group" for doing this. <br>
  Each of the process scrapes product links from each of the book category link. Next, product information are scraped from each link.
 All the information and merged into a list of dictionaries and inserted to the database(bulk insert).
 
## Pytest:
To check the coverage of the tests, run pytest --cov. PyTest was mainly used to test the "api/scrape_site/" api.
If invalid book category presents in the chosen list, the API returns 501. Else it should return 200

## Celery:
Celery was use to run the tasks asynchrnously. We have used single worker and default concurrency[total cpus]

## RabbitMQ: 
This was used as message broker for celery.

## Docker:
Used bind mount to persist the data for PostGres. Celery used 1 worker and highest concurrency. Also logged the celery outputs in a file.
Built 4 containers: web, db, celery, RabbitMQ

## Appmap:
This gives an excellent dynamic overview of the code sequence graph and time spent in different portions of the code.
Also, it shows equivalent SQL queries. I installed the VS code extension and also pip installed appmap. Then, got the appmaps
after running the APIs.




  



