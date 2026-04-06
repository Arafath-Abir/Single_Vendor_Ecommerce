from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Product(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Image upload field
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    # External Image URL field
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    def clean(self):
        # Ensure only one image source is provided
        if self.image and self.image_url:
            raise ValidationError("Provide either an uploaded image or an image URL, not both.")
        
        # Ensure at least one image source is provided
        if not self.image and not self.image_url:
            raise ValidationError("You must provide either an uploaded image or an image URL.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Force validation before saving to database
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def get_image_url(self):
        # Return the priority image source
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return ""

    def average_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg']
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating} by {self.user.username}'
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Cart'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return (self.product.price * self.quantity)
    

class Order(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    # Fixed: IntegerField does not support max_length in Django
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    # Fixed: Phone number should be CharField to avoid issues with leading zeros
    phone = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.first_name} {self.last_name}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return (self.price * self.quantity)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profiles/%Y/%m/%d/', 
        blank=True, 
        null=True,
        default='profiles/default-avatar.jpg'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/%Y/%m/%d/')
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title
