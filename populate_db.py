import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Elanzo.settings")
django.setup()

from shop.models import Category, Product
from django.utils.text import slugify

def populate():
    categories_data = [
        {"name": "Electronics", "description": "Latest gadgets and electronic devices."},
        {"name": "Clothing", "description": "Trendy apparel for men and women."},
        {"name": "Home & Kitchen", "description": "Appliances and decor for your home."},
        {"name": "Sports & Outdoors", "description": "Gear up for your next adventure."},
        {"name": "Beauty & Personal Care", "description": "Skincare, makeup, and more."},
    ]

    products_data = [
        {
            "name": "Wireless Noise Cancelling Headphones",
            "category": "Electronics",
            "price": 15000.00,
            "stock": 50,
            "description": "Experience pure sound with our active noise cancelling over-ear headphones. Features 30-hour battery life and fast charging.",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Smartphone Pro Max",
            "category": "Electronics",
            "price": 120000.00,
            "stock": 20,
            "description": "The ultimate smartphone with an incredible camera system, all-day battery life, and powerful processor.",
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Men's Classic Cotton T-Shirt",
            "category": "Clothing",
            "price": 1200.00,
            "stock": 100,
            "description": "A wardrobe essential. Made from 100% pure premium cotton for ultimate comfort and breathability.",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Women's Denim Jacket",
            "category": "Clothing",
            "price": 3500.00,
            "stock": 40,
            "description": "Classic blue denim jacket with a comfortable fit. Perfect for layering in any season.",
            "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Automatic Espresso Machine",
            "category": "Home & Kitchen",
            "price": 45000.00,
            "stock": 15,
            "description": "Brew cafe-quality espresso and cappuccinos at home with a touch of a button. Features a built-in grinder.",
            "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Non-Stick Cookware Set",
            "category": "Home & Kitchen",
            "price": 8500.00,
            "stock": 30,
            "description": "10-piece premium non-stick aluminum cookware set. Easy to clean and perfect for everyday cooking.",
            "image_url": "https://images.unsplash.com/photo-1584990347449-cd8b824ee1ac?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Yoga Mat with Alignment Lines",
            "category": "Sports & Outdoors",
            "price": 2500.00,
            "stock": 60,
            "description": "Eco-friendly, non-slip yoga mat with alignment markers to perfect your poses. Includes carrying strap.",
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Camping Tent 4-Person",
            "category": "Sports & Outdoors",
            "price": 12000.00,
            "stock": 10,
            "description": "Waterproof, easy-setup dome tent for 4 people. Ideal for family camping trips and outdoor adventures.",
            "image_url": "https://images.unsplash.com/photo-1504280390237-72ce00e408ec?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Hydrating Face Wash",
            "category": "Beauty & Personal Care",
            "price": 950.00,
            "stock": 80,
            "description": "Gentle, non-drying face cleanser infused with hyaluronic acid to keep your skin hydrated and glowing.",
            "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Luxury Perfume For Men",
            "category": "Beauty & Personal Care",
            "price": 5500.00,
            "stock": 25,
            "description": "An elegant and long-lasting masculine fragrance featuring notes of sandalwood, citrus, and musk.",
            "image_url": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?q=80&w=1000&auto=format&fit=crop"
        }
    ]

    for cat_data in categories_data:
        Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"slug": slugify(cat_data["name"]), "description": cat_data["description"]}
        )

    for prod_data in products_data:
        category = Category.objects.get(name=prod_data["category"])
        Product.objects.get_or_create(
            name=prod_data["name"],
            defaults={
                "slug": slugify(prod_data["name"]),
                "description": prod_data["description"],
                "price": prod_data["price"],
                "stock": prod_data["stock"],
                "category": category,
                "image_url": prod_data["image_url"]
            }
        )

    print(f"Successfully added {len(categories_data)} categories and {len(products_data)} products.")

if __name__ == '__main__':
    populate()
