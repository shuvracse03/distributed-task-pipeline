import pytest
from  rest_framework.test import APIClient
from request_app.models import *
from django.db.models import Avg, Count
import time

client = APIClient()

@pytest.mark.django_db
def test_unknown_category1():
    data={"book_types":"Unknown"}
    response = client.post('/api/scrape_site/',data=data, format='json')
    assert response.status_code == 501
    
    
@pytest.mark.django_db
def test_unknown_category2():
    data={"book_types":"Travel,Unknown Category"}
    response = client.post('/api/scrape_site/',data=data, format='json')
    assert response.status_code == 501

@pytest.mark.django_db
def test_single_category():
    data={"book_types":"Travel"}
    response = client.post('/api/scrape_site/',data=data, format='json')
    assert response.status_code == 200    
    
@pytest.mark.django_db
def test_multiple_category():
    data={"book_types":"Travel,Music"}
    response = client.post('/api/scrape_site/',data=data, format='json')
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_all_category():
    data={"book_types":"all"}
    response = client.post('/api/scrape_site/',data=data, format='json')
    assert response.status_code == 200
    
  

