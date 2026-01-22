# Restaurant Management System

**Authors:** Ashraf, Nagham, Shapal, Souad

A complete **Django REST Framework** project for managing users, customers, menu items, and orders with **role-based permissions**, JWT authentication, and fully documented APIs.  

This system allows Admins, Managers, and Staff to perform operations based on their roles, ensuring secure access and workflow management.

---

## Features

- **Users & Roles**
  - Admin: Full CRUD on users, menu, orders, and customers.
  - Manager: Can manage orders (including status updates) and menu (CRUD), read-only on customers.
  - Staff: Read-only access for menu and orders.

- **Menu Management**
  - Categories & Products linked
  - CRUD operations with role-based access
  - Available products endpoint for staff

- **Order Management**
  - Create orders with multiple items
  - Automatic total calculation
  - Status workflow: `New → Preparing → Ready → Delivered`

- **Customer Management**
  - Add, view, update, delete customers
  - Permissions controlled by role

- **Authentication**
  - JWT-based (Access + Refresh tokens)
  - Logout with refresh token blacklist

- **Validation & Security**
  - Input validation on all models
  - Role-based permissions enforced
  - SQL Injection safe (using Django ORM)

- **Testing**
  - Unit tests included for all apps
  - Validates CRUD, permissions, and workflow logic

- **Documentation**
  - Swagger UI and Redoc using **drf-spectacular**
  - Full endpoint summaries and request/response schemas

---

## Sample Data

- **Categories:** Pizza, Drinks, Burgers, Desserts, Salads  
- **Products:** Margherita Pizza, Cola, Cheeseburger, Chocolate Cake, Caesar Salad  
- **Customers:** John Doe, Alice Smith, Bob Brown  

Use Django admin or fixtures to load sample data.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/ashraf171/restaurant-management-system.git
cd restaurant-management-system
Create a virtual environment and activate it

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Apply migrations

python manage.py migrate


Create a superuser

python manage.py createsuperuser


Run the development server

python manage.py runserver

API Endpoints
Users (Admin only)
Method	Endpoint	Description
GET	/api/users/	List all users
POST	/api/users/	Create a new user
GET	/api/users/{id}/	Retrieve user info
PUT	/api/users/{id}/	Update user info
DELETE	/api/users/{id}/	Delete user
Customers
Method	Endpoint	Role	Description
GET	/api/customers/	Admin, Manager	List all customers
POST	/api/customers/	Admin	Create a new customer
GET	/api/customers/{id}/	Admin, Manager	Retrieve customer info
PUT	/api/customers/{id}/	Admin	Update customer info
DELETE	/api/customers/{id}/	Admin	Delete customer
Menu
Categories
Method	Endpoint	Role	Description
GET	/api/categories/	Admin, Manager	List categories
POST	/api/categories/	Admin	Create a category
GET	/api/categories/{id}/	Admin, Manager	Retrieve category
PUT	/api/categories/{id}/	Admin	Update category
DELETE	/api/categories/{id}/	Admin	Delete category
Products
Method	Endpoint	Role	Description
GET	/api/products/	Admin, Manager, Staff	List all products
POST	/api/products/	Admin	Create product
GET	/api/products/{id}/	Admin, Manager, Staff	Retrieve product
PUT	/api/products/{id}/	Admin	Update product
DELETE	/api/products/{id}/	Admin	Delete product
GET	/api/products/available/	Admin, Manager, Staff	List only available products
Orders
Method	Endpoint	Role	Description
GET	/api/orders/	Admin, Manager	List all orders
POST	/api/orders/	Admin	Create new order
GET	/api/orders/{id}/	Admin, Manager	Retrieve order details
PUT	/api/orders/{id}/update_status/	Admin, Manager	Update order status (New → Preparing → Ready → Delivered)
Authentication
Method	Endpoint	Description
POST	/api/token/	Obtain JWT access & refresh tokens
POST	/api/token/refresh/	Refresh access token
POST	/api/logout/	Blacklist refresh token to logout user
Running Tests

Run all tests

python manage.py test


Run tests for a specific app

python manage.py test menu
python manage.py test customers
python manage.py test users
python manage.py test orders


✅ All tests should pass if setup correctly.

Notes

Order total amounts are automatically calculated when creating orders.

Order status transitions are restricted: New → Preparing → Ready → Delivered.

Staff users have read-only access to menu and orders.

Managers can update order status but cannot create users or customers.

JWT authentication is required for all API access.

All endpoints are fully documented with Swagger and Redoc.

API Documentation

Schema: /api/schema/

Swagger UI: /api/docs/