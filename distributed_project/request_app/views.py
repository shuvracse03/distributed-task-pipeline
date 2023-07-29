from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import *
from .tasks import *


# Site to scrape: https://books.toscrape.com/
# curl command: curl -d '{"book_types":"Travel"}' -H "Content-Type: application/json" -X POST http://localhost:8001/api/scrape_site/
# Examples : {"book_types":"Travel"} , {"book_types":"all"}, , {"book_types":"Travel,Fiction"}
#API will return immediately and will trigger celery tasks in the background
class ScrapeSite(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        book_types = request.data.get("book_types", "")
        accepted_types = [
            "Travel",
            "Mystery",
            "Historical Fiction",
            "Sequential Art",
            "Classics",
            "Philosophy",
            "Romance",
            "Womens Fiction",
            "Fiction",
            "Childrens",
            "Religion",
            "Nonfiction",
            "Music",
            "Default",
            "Science Fiction",
            "Sports and Games",
            "Add a comment",
            "Fantasy",
            "New Adult",
            "Young Adult",
            "Science",
            "Poetry",
            "Paranormal",
            "Art",
            "Psychology",
            "Autobiography",
            "Parenting",
            "Adult Fiction",
            "Humor",
            "Horror",
            "History",
            "Food and Drink",
            "Christian Fiction",
            "Business",
            "Biography",
            "Thriller",
            "Contemporary",
            "Spirituality",
            "Academic",
            "Self Help",
            "Historical",
            "Christian",
            "Suspense",
            "Short Stories",
            "Novels",
            "Health",
            "Politics",
            "Cultural",
            "Erotica",
            "Crime",
            "all",
        ]
        if "," not in book_types:
            clean_types = [book_types]
        else:
            clean_types = book_types.split(",")
        for elem in clean_types:
            if elem not in accepted_types: #Check if any user's chosen book category type is invalid, no scraping in that case
                return Response(
                    {"status": "Unknown book category. Cannot process"},
                    status=status.HTTP_501_NOT_IMPLEMENTED,
                )

        scrape_books.delay(book_types)
        return Response({"status": "Scraping started..."}, status=status.HTTP_200_OK)
