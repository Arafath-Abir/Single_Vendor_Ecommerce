import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Elanzo.settings")
django.setup()

from shop.models import Category, Product
from django.utils.text import slugify

def populate_more():
    categories_data = [
        {"name": "Books & Stationery", "description": "A wide selection of books, notebooks, and office supplies."},
        {"name": "Toys & Games", "description": "Fun and educational toys for children of all ages."},
        {"name": "Health & Wellness", "description": "Vitamins, supplements, and personal health products."},
        {"name": "Automotive", "description": "Accessories and tools for your car and bike."},
        {"name": "Fashion Accessories", "description": "Watches, jewelry, bags, and more."},
    ]

    products_data = [
        # Books & Stationery
        {
            "name": "The Great Gatsby - Hardcover",
            "category": "Books & Stationery",
            "price": 850.00,
            "stock": 30,
            "description": "F. Scott Fitzgerald's classic novel in a premium hardcover edition.",
            "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Premium Leather Journal",
            "category": "Books & Stationery",
            "price": 1200.00,
            "stock": 50,
            "description": "Handcrafted leather journal with thick, refillable pages for your daily thoughts.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?q=80&w=1000&auto=format&fit=crop"
        },
        # Toys & Games
        {
            "name": "Mechanical Chess Set",
            "category": "Toys & Games",
            "price": 4500.00,
            "stock": 15,
            "description": "A beautifully designed wooden chess set for enthusiasts and competitive play.",
            "image_url": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Advanced Robotic Kit",
            "category": "Toys & Games",
            "price": 12500.00,
            "stock": 10,
            "description": "Build and program your own robot with this comprehensive STEM education kit.",
            "image_url": "https://images.unsplash.com/photo-1535378917042-10a22c95931a?q=80&w=1000&auto=format&fit=crop"
        },
        # Health & Wellness
        {
            "name": "Multivitamin & Mineral Capsules",
            "category": "Health & Wellness",
            "price": 2200.00,
            "stock": 100,
            "description": "Daily essential nutrients for improved immunity and energy levels.",
            "image_url": "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Aromatherapy Oil Diffuser",
            "category": "Health & Wellness",
            "price": 3800.00,
            "stock": 25,
            "description": "Ultrasonic diffuser with LED lights for a relaxing and peaceful home atmosphere.",
            "image_url": "https://images.unsplash.com/photo-1602928321679-560bb453f190?q=80&w=1000&auto=format&fit=crop"
        },
        # Automotive
        {
            "name": "Universal Phone Mount for Car",
            "category": "Automotive",
            "price": 1500.00,
            "stock": 40,
            "description": "Sturdy and adjustable phone holder for safe GPS navigation while driving.",
            "image_url": "https://images.unsplash.com/photo-1610647752706-3bb12232b3ab?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Portable Car Vacuum Cleaner",
            "category": "Automotive",
            "price": 4800.00,
            "stock": 20,
            "description": "High-power handheld vacuum cleaner to keep your car interior spotless.",
            "image_url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=1000&auto=format&fit=crop"
        },
        # Fashion Accessories
        {
            "name": "Classic Gold Wristwatch",
            "category": "Fashion Accessories",
            "price": 18000.00,
            "stock": 8,
            "description": "A minimalist and elegant gold-plated watch for any formal or casual occasion.",
            "image_url": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=1000&auto=format&fit=crop"
        },
        {
            "name": "Sunglasses - Aviator Black",
            "category": "Fashion Accessories",
            "price": 3500.00,
            "stock": 35,
            "description": "Timeless aviator style sunglasses with UV protection and polarized lenses.",
            "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=1000&auto=format&fit=crop"
        },
    ]

    for cat_data in categories_data:
        Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"slug": slugify(cat_data["name"]), "description": cat_data["description"]}
        )

    for prod_data in products_data:
        try:
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
        except Exception as e:
            print(f"Error adding {prod_data['name']}: {e}")

    print(f"Successfully added {len(categories_data)} more categories and {len(products_data)} more products.")

if __name__ == '__main__':
    populate_more()
