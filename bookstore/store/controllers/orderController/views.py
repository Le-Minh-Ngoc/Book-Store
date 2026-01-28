"""
Views for order module
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from store.models.book.models import Book
from store.models.order.models import Cart, CartItem, Order, OrderItem, Payment, Shipping, Rating
from store.models.customer.models import Customer


def cart(request):
    """
    View shopping cart
    """
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            
            # Get all items in the cart
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Add item_total to each cart_item
            for item in cart_items:
                item.item_total = item.book.price * item.quantity
            
            # Calculate total
            total = sum(item.book.price * item.quantity for item in cart_items)
            
            context = {
                'cart_items': cart_items,
                'total': total
            }
        except Customer.DoesNotExist:
            context = {'cart_items': [], 'total': 0}
            messages.error(request, 'Customer profile not found')
        
        return render(request, 'cart/view.html', context=context)
    else:
        messages.error(request, 'Please login to view your cart')
        return redirect('customer:login')


def add_to_cart(request, book_id):
    """
    Add a book to the shopping cart
    """
    if request.user.is_authenticated:
        try:
            book = get_object_or_404(Book, id=book_id)
            customer = Customer.objects.get(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            
            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                book=book,
                defaults={'quantity': 1}
            )
            
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            
            messages.success(request, f'{book.title} added to cart!')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found')
            return redirect('customer:login')
    else:
        messages.error(request, 'Please login to add items to cart')
        return redirect('customer:login')
    
    return redirect('order:cart')


def remove_from_cart(request, item_id):
    """
    Remove an item from the shopping cart
    """
    if request.user.is_authenticated:
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            customer = Customer.objects.get(user=request.user)
            
            # Verify that the item belongs to the user's cart
            if cart_item.cart.customer == customer:
                cart_item.delete()
                messages.success(request, 'Item removed from cart!')
            else:
                messages.error(request, 'Unauthorized access')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found')
    else:
        messages.error(request, 'Please login to manage your cart')
    
    return redirect('order:cart')


def checkout(request):
    """
    Checkout process
    """
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            
            if created or not cart.items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('order:cart')
            
            # Get all items in the cart
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Add item_total to each cart_item
            for item in cart_items:
                item.item_total = item.book.price * item.quantity
            
            # Calculate total
            subtotal = sum(item.book.price * item.quantity for item in cart_items)
            shipping_fee = 5.00  # Fixed shipping fee for simplicity
            total = subtotal + shipping_fee
            
            context = {
                'cart_items': cart_items,
                'subtotal': subtotal,
                'shipping_fee': shipping_fee,
                'total': total
            }
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found')
            return redirect('customer:login')
        
        return render(request, 'order/checkout.html', context=context)
    else:
        messages.error(request, 'Please login to checkout')
        return redirect('customer:login')


def place_order(request):
    """
    Place an order
    """
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            
            if created or not cart.items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('order:cart')
            
            # Calculate total
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.book.price * item.quantity for item in cart_items)
            
            # Create order
            order = Order.objects.create(
                customer=customer,
                total_price=total_price
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.book.price,
                    total=cart_item.book.price * cart_item.quantity
                )
            
            # Create payment and shipping records
            payment = Payment.objects.create(
                order=order,
                amount=total_price,
                status='pending'
            )
            
            shipping = Shipping.objects.create(
                order=order,
                fee=5.00,
                status='pending'
            )
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('order:order_history')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found')
            return redirect('customer:login')
    else:
        messages.error(request, 'Invalid request')
        return redirect('order:cart')


def order_history(request):
    """
    View order history
    """
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            orders = Order.objects.filter(customer=customer).order_by('-order_date')
            
            context = {
                'orders': orders
            }
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found')
            context = {'orders': []}
        
        return render(request, 'order/history.html', context=context)
    else:
        messages.error(request, 'Please login to view order history')
        return redirect('customer:login')


def recommendations(request):
    """
    Recommend books based on purchase history and ratings
    """
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)

            # Get the recommendation function
            recommended_books = recommend_books_for_customer(customer)

            context = {
                'recommended_books': recommended_books
            }
        except Customer.DoesNotExist:
            context = {'recommended_books': []}
            messages.error(request, 'Customer profile not found')

        return render(request, 'order/recommendations.html', context=context)
    else:
        messages.error(request, 'Please login to see recommendations')
        return redirect('customer:login')


def recommend_books_for_customer(customer):
    """
    Function to recommend books based on customer's purchase history and ratings
    """
    # Get books from customer's past orders
    order_items = OrderItem.objects.filter(order__customer=customer).select_related('book')
    purchased_book_ids = [item.book.id for item in order_items]

    if not purchased_book_ids:
        # If no purchase history, recommend top-rated books
        from store.models.order.models import Rating
        from django.db.models import Avg

        top_rated_books = Book.objects.annotate(avg_rating=Avg('rating__score')).filter(
            avg_rating__isnull=False
        ).order_by('-avg_rating')[:4]

        return list(top_rated_books)

    # Find other customers who bought similar books
    # Get all orders that contain books the customer has purchased
    similar_customers_orders = OrderItem.objects.filter(
        book_id__in=purchased_book_ids
    ).select_related('order__customer').exclude(
        order__customer=customer
    )

    # Get the customers who made these orders
    similar_customer_ids = [item.order.customer.id for item in similar_customers_orders]

    # Find books that these similar customers have purchased
    recommended_books = set()
    if similar_customer_ids:
        books_bought_by_similar = OrderItem.objects.filter(
            order__customer_id__in=similar_customer_ids
        ).exclude(
            book_id__in=purchased_book_ids
        ).select_related('book')

        # Sort by frequency of appearance among similar customers
        book_frequency = {}
        for item in books_bought_by_similar:
            if item.book.id not in book_frequency:
                book_frequency[item.book.id] = 0
            book_frequency[item.book.id] += 1

        # Sort books by frequency and get top 4
        sorted_books = sorted(book_frequency.items(), key=lambda x: x[1], reverse=True)
        recommended_book_ids = [book_id for book_id, freq in sorted_books[:4]]

        recommended_books = Book.objects.filter(id__in=recommended_book_ids)
    else:
        # If no similar customers found, recommend based on ratings of similar categories
        from django.db.models import Avg

        # Get categories of books the customer has purchased
        purchased_categories = Book.objects.filter(
            id__in=purchased_book_ids
        ).values_list('category', flat=True).distinct()

        # Recommend top-rated books in these categories
        recommended_books = Book.objects.filter(
            category__in=purchased_categories
        ).annotate(avg_rating=Avg('rating__score')).filter(
            avg_rating__isnull=False
        ).exclude(
            id__in=purchased_book_ids
        ).order_by('-avg_rating')[:4]

    return list(recommended_books)