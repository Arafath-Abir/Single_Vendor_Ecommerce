<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0.2-ff6a00?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SSLCommerz-Payment-ff6a00?style=for-the-badge" alt="SSLCommerz">
  <img src="https://img.shields.io/badge/License-MIT-e63946?style=for-the-badge" alt="MIT">
</p>

<br/>

<h1 align="center">
  🛍️ Elanzo
</h1>

<p align="center">
  <strong>A premium, full-featured single-vendor e-commerce platform built with Django.</strong><br/>
  Seamless shopping experience with an integrated seller dashboard, secure payment gateway, and a stunning admin panel.
</p>

<p align="center">
  <a href="#-features">Features</a> ·
  <a href="#-tech-stack">Tech Stack</a> ·
  <a href="#-project-structure">Project Structure</a> ·
  <a href="#-getting-started">Getting Started</a> ·
  <a href="#-environment-variables">Environment Variables</a> ·
  <a href="#-screenshots">Screenshots</a>
</p>

---

## ✨ Features

### 🛒 Customer Side
- **Product Browsing** — Filter by category, price range, and star rating
- **Smart Search** — Full-text search across product names, descriptions, and categories
- **Recently Viewed** — Session-based product history tracking
- **Shopping Cart** — Ajax-powered live cart updates with quantity management
- **Checkout & Payment** — Full SSLCommerz payment gateway integration (sandbox + production)
- **Order Tracking** — User dashboard with real-time order status (Pending → Delivered)
- **Ratings & Reviews** — Only verified buyers (paid orders) can leave reviews
- **Google OAuth** — One-click sign in via Google via django-allauth
- **User Profile** — Edit personal info, update profile picture, change password

### 🧑‍💼 Seller Dashboard
- **Analytics Overview** — Total revenue, orders, products, users at a glance
- **Top Selling Products** — Ranked by total units sold
- **Top Customers** — Ranked by total amount spent
- **Recent Orders & Reviews** — Quick snapshot of latest activity
- **Product Management** — Full CRUD with image support (upload or URL)
- **Category Management** — Manage product taxonomy
- **Order Management** — Update order status in real-time
- **Banner Management** — Control homepage hero banners
- **Profile Picture** — Staff-specific profile picture management

### 🔐 Django Admin Panel (Unfold UI)
- **Premium Unfold Theme** — Custom orange color palette matching the site branding
- **Smart Sidebar** — Grouped navigation with Material Symbols icons
- **All Models Themed** — Products, Orders, Users, Auth, Sites, Allauth all use Unfold
- **Status Badges** — Visual labels for product availability
- **Date Hierarchy** — Easy date-based order filtering
- **Search & Filters** — Every model has relevant search and filter capabilities

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0.2 |
| **Database** | PostgreSQL 16 (psycopg2-binary) |
| **Authentication** | Django Auth + django-allauth (Google OAuth) |
| **Payment Gateway** | SSLCommerz (sslcommerz-lib) |
| **Admin UI** | django-unfold |
| **Image Handling** | Pillow |
| **Email** | Gmail SMTP |
| **Environment** | python-dotenv |
| **Production Server** | Gunicorn |
| **Frontend** | Vanilla HTML/CSS/JS with Inter font |

---

## 📁 Project Structure

```
Elanzo/
├── Mallava/                        # Django project root
│   ├── Elanzo/                     # Core settings package
│   │   ├── settings.py             # Project settings (env-driven)
│   │   ├── urls.py                 # Root URL configuration
│   │   └── wsgi.py
│   │
│   ├── shop/                       # Main application
│   │   ├── admin.py                # Custom Unfold admin registrations
│   │   ├── context_processors.py   # Cart item count injector
│   │   ├── forms.py                # All application forms
│   │   ├── models.py               # Data models
│   │   ├── sslcommerz.py           # Payment gateway logic
│   │   ├── urls.py                 # App URL patterns
│   │   └── views.py                # All views
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html               # Base layout
│   │   ├── home.html               # Homepage with banners
│   │   ├── product_list.html       # Product catalog
│   │   ├── product_detail.html     # Product detail + ratings
│   │   ├── cart_detail.html        # Shopping cart
│   │   ├── checkout.html           # Checkout form
│   │   ├── payment_success.html    # Post-payment confirmation
│   │   ├── profile.html            # User profile + order history
│   │   ├── emails/                 # Email templates
│   │   │   └── order_confirmation.html
│   │   └── dashboard/              # Seller dashboard templates
│   │       ├── dashboard_base.html
│   │       ├── index.html
│   │       ├── manage_products.html
│   │       ├── manage_orders.html
│   │       ├── manage_categories.html
│   │       ├── manage_banners.html
│   │       └── profile_form.html
│   │
│   ├── static/                     # Static assets
│   │   └── css/
│   │       ├── base.css            # Global design system (orange/red theme)
│   │       ├── dashboard.css       # Seller dashboard styles
│   │       ├── home.css
│   │       ├── product_detail.css
│   │       ├── cart.css
│   │       └── auth.css
│   │
│   ├── media/                      # User-uploaded files
│   ├── .env                        # 🔒 Local secrets (not committed)
│   ├── .env.example                # ✅ Safe template to share
│   ├── .gitignore
│   ├── manage.py
│   └── requirements.txt
```

---

## 🗂 Data Models

```
Category  ──< Product ──< OrderItem >── Order ── User
                  |                               |
                  └──< CartItem >── Cart ──────────
                  |
                  └──< Rating ── User

User ──── Profile          (profile picture)
User ──── Banner           (homepage banners, admin-managed)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Arafath-Abir/Single_Vendor_Ecommerce.git
cd Single_Vendor_Ecommerce/Mallava
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Open .env and fill in your actual values
```

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE mallava_db;
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** for the storefront and **http://127.0.0.1:8000/admin/** for the admin panel.

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and set the values:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | `True` for dev, `False` for prod | ✅ |
| `ALLOWED_HOSTS` | Comma-separated list of hosts | ✅ |
| `DB_NAME` | PostgreSQL database name | ✅ |
| `DB_USER` | PostgreSQL user | ✅ |
| `DB_PASSWORD` | PostgreSQL password | ✅ |
| `DB_HOST` | Database host | ✅ |
| `DB_PORT` | Database port (default: 5432) | ✅ |
| `EMAIL_HOST_USER` | Gmail address for sending emails | ✅ |
| `EMAIL_HOST_PASSWORD` | Gmail App Password | ✅ |
| `SSL_COMMERZE_STORE_ID` | SSLCommerz store ID | ✅ |
| `SSL_COMMERZE_STORE_PASSWORD` | SSLCommerz store password | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Optional |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Optional |

> **⚠️ Warning:** Never commit your `.env` file. It is automatically excluded by `.gitignore`.

---

## 💳 Payment Gateway

This project uses **SSLCommerz** (the most popular payment gateway in Bangladesh).

- Sandbox mode is enabled by default in the `.env.example`
- Switch to production by changing the `SSL_COMMERZE_PAYMENT_URL` and `SSL_COMMERZE_VALIDATION_URL` to their production equivalents
- Supported: card payments, mobile banking (bKash, Nagad, Rocket), net banking

---

## 🎨 Color Palette

The design system is built around a warm, energetic orange palette:

| Role | Color | Hex |
|------|-------|-----|
| **Primary** | Vibrant Orange | `#ff6a00` |
| **Accent** | Deep Red | `#e63946` |
| **Background** | Off-White | `#fff9f2` |
| **Dark** | Warm Dark | `#2b1f1c` |
| **Secondary** | Muted Brown | `#78716c` |

---

## 📧 Email Notifications

Order confirmation emails are sent automatically after successful payment. Templates are located in `templates/emails/`.

To configure Gmail:
1. Enable 2-Factor Authentication on your Google account
2. Generate an **App Password** (Google Account → Security → App Passwords)
3. Set `EMAIL_HOST_PASSWORD` to that App Password in `.env`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Arafath-Abir">Arafath Abir</a>
</p>
