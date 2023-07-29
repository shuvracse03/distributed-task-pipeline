from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .tasks import *

# Create your views here.
#https://books.toscrape.com/
#curl -d '{"book_types":"Travel,Mystery, Historical Fiction"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/scrape_site/
class ScrapeSite(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        book_types = request.data.get('book_types','')
        print(book_types)
        scrape_books.delay(book_types)
        return Response({'success':'Scraped successfully'})
