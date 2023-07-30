import pytest
from rest_framework.test import APIClient
from request_app.models import *
from request_app.tasks import *

import time

client = APIClient()


# Test: Get all book categories
def test_all_category():
    n_categories = len(get_book_categories().keys())
    assert n_categories == 50


# Test :get a book's information
def test_get_book_info():
    url = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    parent_url = (
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    )
    n_values = len(get_book_info(url, parent_url).keys())
    assert n_values == 11


# Test :get all links from a categories' page
def test_get_links_from_pages():
    page_no = 1
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    n_links = len(get_links_from_pages(page_no, url))
    assert n_links == 11


# Test :get all links for a category(can be multi/single page)
def test_get_product_links():
    url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    n_links = len(get_product_links(url))
    assert n_links == 32


# Test :Insert json list to db
@pytest.mark.django_db
def test_insert_to_db():
    info = {
        "title": "Test Title",
        "description": "This is test description",
        "upc": "127283434",
        "product_type": "Book",
        "price_include_tax": 1234.5,
        "price_exclude_tax": 1234.5,
        "currency": "USD",
        "tax": 0,
        "stock": 10,
        "no_reviews": 89,
        "parent_url": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    }
    json_list = [info]
    insert_to_db(json_list)
    count = Product.objects.count()
    assert count == 1


# Test :Test scraping categories
def test_scrape_books():
    try:
        chosen_cats = scrape_books("Travel,Mystery")
        assert len(chosen_cats) == 2
    except:
        assert False


# Test : process link
@pytest.mark.django_db
def test_process_link():
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    process_link(url)
    count = Product.objects.count()
    assert count == 11
