# Restaurant Management System

**Author:** Ashraf, Nagham, Shapal, Souad

A complete Django REST Framework project to manage menu items, orders, customers, and users with role-based permissions. This project includes authentication, role-based permissions, CRUD operations for all main models, automated order total calculation, and a complete API ready for testing.

This system manages:

- Users with roles: Admin, Manager, Staff
- Customers
- Menu (Categories & Products)
- Orders (including order items and status workflow)

---

## Features

- Admin: Full CRUD on users, menu, orders, and customers.
- Manager: Read-only access to customers, orders, and menu; can update order statuses.
- Staff: Read-only access for menu and orders.
- Menu Management: Categories and products linked, full CRUD, role-based permissions.
- Order Management: Create orders with multiple items, automatic total calculation, status workflow: New → Preparing → Ready → Delivered.
- Customer Management: Add, view, update, delete customers; permissions controlled by role.
- JWT Authentication: Only authenticated users can access APIs.
- Role-based permissions applied on each endpoint.
- Unit tests included for all apps (menu, customers, users, orders).

---

## Sample Data

- Categories: Pizza, Drinks, Burgers, Desserts, Salads
- Products: Margherita Pizza, Cola, Cheeseburger, Chocolate Cake, Caesar Salad
- Customers: John Doe, Alice Smith, Bob Brown

Use Django admin or fixtures to load sample data.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ashraf171/restaurant-management-system.git
cd restaurant-management-system
Create a virtual environment and activate it:

bash
Copy code
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
API Endpoints
Users
/users/ [GET] - Admin - List all users

/users/ [POST] - Admin - Create a new user

/users/{id}/ [GET] - Admin - Retrieve user info

/users/{id}/ [PUT] - Admin - Update user info

/users/{id}/ [DELETE] - Admin - Delete user

Customers
/customers/customers/ [GET] - Admin, Manager - List all customers

/customers/customers/ [POST] - Admin - Create a new customer

/customers/customers/{id}/ [GET] - Admin, Manager - Retrieve customer info

/customers/customers/{id}/ [PUT] - Admin - Update customer info

/customers/customers/{id}/ [DELETE] - Admin - Delete customer

Menu
/menu/categories/ [GET] - Admin, Manager - List categories

/menu/categories/ [POST] - Admin - Create a category

/menu/categories/{id}/ [GET] - Admin, Manager - Retrieve category

/menu/categories/{id}/ [PUT] - Admin - Update category

/menu/categories/{id}/ [DELETE] - Admin - Delete category

/menu/products/ [GET] - Admin, Manager, Staff - List products

/menu/products/ [POST] - Admin - Create product

/menu/products/{id}/ [GET] - Admin, Manager, Staff - Retrieve product

/menu/products/{id}/ [PUT] - Admin - Update product

/menu/products/{id}/ [DELETE] - Admin - Delete product

Orders
/orders/orders/ [GET] - Admin, Manager - List orders

/orders/orders/ [POST] - Admin - Create a new order

/orders/orders/{id}/ [GET] - Admin, Manager - Retrieve order details

/orders/orders/{id}/update_status/ [PUT] - Admin, Manager - Update order status

Authentication
JWT-based authentication

Only authenticated users can access the APIs

Role-based access control applied to each endpoint

Running Tests
Run all tests:

bash
Copy code
python manage.py test
Run tests for a specific app:

bash
Copy code
python manage.py test menu
python manage.py test customers
python manage.py test users
python manage.py test orders
Notes
Order total amounts are automatically calculated when creating orders.

Order status transitions are restricted: New → Preparing → Ready → Delivered.

Staff users have read-only access to menu and orders.

Managers can update order status but cannot create users or customers.