"""
Views for book module
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from store.models.book.models import Book


def index(request):
    """
    Display list of all books
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'book/index.html', context=context)


def detail(request, book_id):
    """
    Display details of a specific book
    """
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book
    }
    return render(request, 'book/detail.html', context=context)


def search(request):
    """
    Search for books
    """
    query = request.GET.get('q')
    books = []
    
    if query:
        books = Book.objects.filter(title__icontains=query) | \
                Book.objects.filter(author__name__icontains=query) | \
                Book.objects.filter(category__type__icontains=query)
    
    context = {
        'books': books,
        'query': query
    }
    return render(request, 'book/search_results.html', context=context)