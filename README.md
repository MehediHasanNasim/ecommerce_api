# 🛍️ E-Commerce REST API

[![Django](https://img.shields.io/badge/Django-5.2.3-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.0-blue.svg)](https://www.django-rest-framework.org/)
[![Stripe](https://img.shields.io/badge/Stripe-12.2.0-yellow.svg)](https://stripe.com/)

A full-featured e-commerce API with user authentication, product management, Stripe payments, and Google OAuth integration.

## ✨ Features

| Feature                | Status |
|------------------------|--------|
| JWT Authentication     | ✅     |
| Email Verification     | ✅     |
| Password Reset         | ✅     |
| Google OAuth           | ✅     |
| Product Catalog        | ✅     |
| Category Filtering     | ✅     |
| Search Functionality   | ✅     |
| Shopping Cart          | ✅     |
| Stripe Checkout        | ✅     |
| AWS S3 Media Storage   | ✅     |
| Book Scraper (Bonus)   | ✅     |
| Review System (Bonus)  | ✅     |

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+
- PostgreSQL
- Stripe Account
- Google OAuth Credentials
- AWS S3 Bucket (Optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-api.git
   cd ecommerce-api
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
5. Configure environment variables
   ```bash
   cp .env.example .env
6. Run migrations
   ```bash
   python manage.py migrate
7. Create superuser
   ```bash
   python manage.py createsuperuser
8. Start development server
   ```bash
   python manage.py runserver
API Documentation
   ```bash
   Import the Postman collection from docs/ecommerce_api_postman.json


