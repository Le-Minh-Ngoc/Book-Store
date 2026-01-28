"""
Views for staff module
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models.book.models import Book, Author, Publisher, Category
from store.models.staff.models import Staff


def index(request):
    """
    Staff dashboard
    """
    if request.user.is_authenticated and hasattr(request.user, 'staff'):
        # Count books and other stats
        book_count = Book.objects.count()
        context = {
            'book_count': book_count
        }
        return render(request, 'staff/dashboard.html', context=context)
    else:
        messages.error(request, 'Access denied. Staff only.')
        return redirect('book:index')


def add_book(request):
    """
    Staff view to add new books to inventory
    """
    if request.method == 'POST':
        # Process form to add new book
        title = request.POST['title']
        author_id = request.POST['author']
        price = request.POST['price']
        instock = request.POST['instock']
        publisher_id = request.POST['publisher']
        category_id = request.POST['category']
        
        # Get related objects
        author = Author.objects.get(id=author_id)
        publisher = Publisher.objects.get(id=publisher_id)
        category = Category.objects.get(type=category_id)
        
        # Create new book
        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            instock=instock,
            publisher=publisher,
            category=category
        )
        
        messages.success(request, f'Book "{title}" added successfully!')
        return redirect('staff:inventory')
    
    # Get all authors, publishers, and categories for the form
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    categories = Category.objects.all()
    
    context = {
        'authors': authors,
        'publishers': publishers,
        'categories': categories
    }
    
    return render(request, 'staff/add_book.html', context=context)


def inventory(request):
    """
    View to manage book inventory
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'staff/inventory.html', context=context)