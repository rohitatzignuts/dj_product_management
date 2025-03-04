# Task and Product Management System API

## Overview
This project is a **Django REST Framework (DRF)** based API for managing products, categories, and subcategories. It includes authentication, soft deletes, rate limiting, and email notifications using Mailtrap.

## Features
- **Authentication & Authorization**
  - Uses **Djoser** for authentication and user management.
  - Implements **SimpleJWT** for token-based authentication.
  - Supports user login, registration, password reset, and token refresh.
  
- **API Documentation**
  - Integrated **Swagger UI** for interactive API documentation.

- **Product, Task & Category Management**
  - CRUD operations for products, categories, tasks and subcategories.
  - Soft delete implementation to mark entities as deleted instead of removing them.
  
- **Email Notifications**
  - Uses **Mailtrap** for testing email notifications.
  - Sends password reset emails and other system-generated notifications.

- **Rate Limiting**
  - Configured rate limiting for various API endpoints to prevent abuse.

- **Indexing for Performance**
  - Indexed database fields for faster queries.

## Installation
### Prerequisites
- Python 3.12+
- Django 5+
- PostgreSQL (recommended) or SQLite
- Virtual environment (venv)

### Setup Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/rohitatzignuts/dj_product_management.git
   cd product-management-api
   ```

2. **Create and Activate Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables For Mailtrap**

   ```sh
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "sandbox.smtp.mailtrap.io"
    EMAIL_HOST_USER = "EMAIL_HOST_USER"
    EMAIL_HOST_PASSWORD = "EMAIL_HOST_PASSWORD"
    EMAIL_PORT = "EMAIL_PORT"
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    DEFAULT_FROM_EMAIL = "DEFAULT_FROM_EMAIL"
   ```

5. **Set Up Database**

   ```py
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DB_NAME",
        "USER": "USERNAME",
        "PASSWORD": "PASSWORD",
        "HOST": "127.0.0.1",
        "PORT": "PORT",
        }
    }
   ```

6. **Run Migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a Superuser** (optional for admin access)
   ```sh
   python manage.py createsuperuser
   ```

8. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### Authentication
- `POST /auth/users/` - Register a new user.
- `POST /auth/jwt/create/` - Obtain access & refresh tokens.
- `POST /auth/jwt/refresh/` - Refresh access token.
- `POST /auth/users/reset_password/` - Request password reset.
- `POST /auth/token/logout/` - Logout.

### Categories
- `GET /api/categories/` - List all categories.
- `POST /api/categories/` - Create a new category.
- `GET /api/categories/{id}/` - Get a category.
- `PUT /api/categories/{id}/` - Update a category.
- `DELETE /api/categories/{id}/` - Soft delete a category.

### Sub Categories
- `GET /api/subcategories/` - List all sub categories.
- `POST /api/subcategories/` - Create a new sub category.
- `GET /api/subcategories/{id}/` - Get a sub category.
- `PUT /api/subcategories/{id}/` - Update a sub category.
- `DELETE /api/subcategories/{id}/` - Soft delete a sub category.

### Products
- `GET /api/products/` - List all products.
- `POST /api/products/` - Create a new product.
- `GET /api/products/{id}/` - Get a product.
- `PUT /api/products/{id}/` - Update a product.
- `DELETE /api/products/{id}/` - Soft delete a product.

### Products
- `GET /api/products/` - List all products.
- `POST /api/products/` - Create a new product.
- `GET /api/products/{id}/` - Get a product.
- `PUT /api/products/{id}/` - Update a product.
- `DELETE /api/products/{id}/` - Soft delete a product.

## Testing
Run test cases using:
```sh
python manage.py test
```
Run specific test files:
```sh
python manage.py test products.tests.test_auth
```

## Swagger API Documentation
Access interactive documentation at:
```
http://127.0.0.1:8000/swagger/
```


---
### Contributors
- **Rohit Vispute**


