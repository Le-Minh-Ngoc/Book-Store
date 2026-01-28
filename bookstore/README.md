# Bookstore Management System

A comprehensive bookstore management system built with Django using the Domain Package MVC architecture.

## Features

- Customer registration and login
- Browse and search books
- Shopping cart functionality
- Order placement and history
- Staff management interface
- Book inventory management
- Personalized book recommendations
- Rating system

## Architecture

The system follows a Domain Package MVC architecture with the following modules:

- **Book**: Manages books, authors, publishers, and categories
- **Customer**: Handles customer accounts and profiles
- **Staff**: Provides staff interface for inventory management
- **Order**: Manages shopping carts, orders, payments, and shipping

## Prerequisites

- Python 3.8+
- Django 4.0+

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd bookstore
   ```

2. Install Django:
   ```
   pip install django
   ```

3. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser account:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Customers:
- Register an account or log in
- Browse books using the navigation menu
- Search for specific books
- Add books to your cart
- Proceed to checkout to place an order
- View your order history

### For Staff:
- Log in with staff credentials
- Access the staff dashboard
- Add new books to inventory
- Manage existing inventory
- View reports (coming soon)

### For Administrators:
- Access the Django admin panel
- Manage users, books, orders, and other data
- Configure system settings

## Database Schema

The system uses SQLite by default but can be configured to use MySQL or PostgreSQL.
The schema includes tables for users, books, authors, publishers, customers, orders, 
payments, shipping, ratings, and inventory management.

## Project Structure

```
bookstore/
├── manage.py
├── bookstore/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── __init__.py
    ├── apps.py
    ├── models/
    │   ├── __init__.py
    │   ├── book/
    │   │   ├── __init__.py
    │   │   └── models.py
    │   ├── customer/
    │   │   ├── __init__.py
    │   │   └── models.py
    │   ├── staff/
    │   │   ├── __init__.py
    │   │   └── models.py
    │   └── order/
    │       ├── __init__.py
    │       ├── models.py
    │       └── supply_models.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── bookController/
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── customerController/
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── staffController/
    │   │   ├── __init__.py
    │   │   └── views.py
    │   └── orderController/
    │       ├── __init__.py
    │       └── views.py
    ├── templates/
    │   ├── base.html
    │   ├── book/
    │   ├── cart/
    │   ├── customer/
    │   ├── order/
    │   └── staff/
    └── urls/
        ├── __init__.py
        ├── book_urls.py
        ├── customer_urls.py
        ├── staff_urls.py
        └── order_urls.py
```

## Recommendations Algorithm

The system implements a recommendation engine that suggests books based on:
- Purchase history of similar customers
- Ratings of books in similar categories
- Top-rated books when no history is available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.