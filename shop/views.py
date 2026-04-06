from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
User = get_user_model()
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, RatingForm, CheckoutForm, ProductForm, CategoryForm, BannerForm, ProfileForm
from . import models
from .models import Category, Product, Rating, Cart, CartItem, Order, OrderItem, Banner, Profile
from django.db.models import Avg, Min, Max, Q, Sum, Count
from . import sslcommerz
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm() 
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

def home_view(request):
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    recent_ids = request.session.get('recently_viewed', [])
    recently_viewed_products = sorted(
        Product.objects.filter(id__in=recent_ids),
        key=lambda p: recent_ids.index(p.id)
    )
    active_banners = Banner.objects.filter(active=True).order_by('order', 'created_at')
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'recently_viewed_products': recently_viewed_products,
        'banners': active_banners,
    }
    return render(request, 'home.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    min_price = products.aggregate(Min('price'))['price__min']
    max_price = products.aggregate(Max('price'))['price__max']
    if request.GET.get('min_price'):
        products = products.filter(price__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        products = products.filter(price__lte=request.GET['max_price'])
    if request.GET.get('rating'):
        products = products.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=request.GET['rating'])
    if request.GET.get('search'):
        query = request.GET.get('search')
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'product_list.html', {
        'category': category, 
        'categories': categories, 
        'products': products, 
        'min_price': min_price, 
        'max_price': max_price
        })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)
    request.session['recently_viewed'] = recently_viewed[:5]
    user_rating = None
    rating_form = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(product=product, user=request.user)
        except Rating.DoesNotExist:
            pass
        rating_form = RatingForm(instance=user_rating)
    return render(request, 'product_detail.html', {
        'product': product, 
        'related_products': related_products,
        'user_rating': user_rating,
        'rating_form': rating_form
        })

def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ordered_item = OrderItem.objects.filter(order__user=request.user, product=product, order__paid=True)
    if not ordered_item.exists():
        messages.error(request, 'You can only rate products you have purchased.')
        return redirect('product_detail', slug=product.slug)
    try:
        rating = Rating.objects.get(product=product, user=request.user)
        form = RatingForm(request.POST, instance=rating)
    except Rating.DoesNotExist:
        form = RatingForm(request.POST)
    if form.is_valid():
        new_rating = form.save(commit=False)
        new_rating.product = product
        new_rating.user = request.user
        new_rating.save()
        messages.success(request, 'Your rating has been submitted.')
    return redirect('product_detail', slug=product.slug)

def cart_add(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to add products to your cart.')
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.name} to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

def cart_update(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            item_deleted = True
        else:
            cart_item.quantity = quantity
            cart_item.save()
            item_deleted = False
            
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'item_total': cart_item.get_cost() if not item_deleted else 0,
                'cart_total': cart.get_total_cost(),
                'total_items': cart.get_total_items(),
                'item_deleted': item_deleted
            })
            
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_detail')

def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return redirect('product_list')
    except Cart.DoesNotExist:
        return redirect('product_list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
            cart.items.all().delete()
            request.session['order_id'] = order.id
            return redirect('payment_process')
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form, 'cart': cart})

def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')
    order = get_object_or_404(Order, id=order_id)
    
    response_data = sslcommerz.generate_ssl_commerz_payment(request, order)
    if response_data and response_data.get('status') == 'SUCCESS':
        return redirect(response_data.get('GatewayPageURL'))
    else:
        messages.error(request, 'Failed to initiate payment. Please try again.')
        return redirect('checkout')

@csrf_exempt
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.status = 'processing'
    tran_id = request.POST.get('tran_id')
    if tran_id:
        order.transaction_id = tran_id
    else:
        order.transaction_id = f'TXN{order.id}{order.created_at.strftime("%Y%m%d%H%M%S")}'
    order.save()
    for item in order.order_items.all():
        item.product.stock = max(0, item.product.stock - item.quantity)
        item.product.save()
        
    try:
        sslcommerz.send_order_confirmation_email(order)
    except Exception as e:
        print(f"Email error: {e}")
        
    messages.success(request, 'Payment successful!')
    return render(request, 'payment_success.html', {'order': order})

@csrf_exempt
def payment_fail(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if order:
        order.status = 'canceled'
        order.save()
    messages.error(request, 'Payment failed.')
    return redirect('home')

@csrf_exempt
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'canceled'
    order.save()
    messages.info(request, 'Order canceled.')
    return redirect('home')

# User Dashboard & Profile
@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    running_orders = user_orders.filter(status__in=['pending', 'processing', 'shipped'])
    order_history = user_orders.filter(status__in=['delivered', 'canceled'])
    return render(request, 'profile.html', {
        'running_orders': running_orders,
        'order_history': order_history,
        'total_orders': user_orders.count()
    })

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



# Seller dashboard
@staff_member_required
def seller_dashboard(request):
    # Summary Statistics
    total_revenue = Order.objects.filter(paid=True).aggregate(Sum('order_items__price'))['order_items__price__sum'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()
    low_stock_products = Product.objects.filter(stock__lte=5)

    # Top Selling Products (by quantity)
    top_selling = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

    # Recent Data
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    # Recent Reviews
    recent_reviews = Rating.objects.all().order_by('-created_at')[:5]

    # Top Customers (by total spent)
    top_customers = User.objects.annotate(
        total_spent=Sum('order__order_items__price', filter=Q(order__paid=True))
    ).filter(total_spent__gt=0).order_by('-total_spent')[:5]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'low_stock': low_stock_products.count(),
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_products,
        'top_selling': top_selling,
        'recent_reviews': recent_reviews,
        'top_customers': top_customers,
    }
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def manage_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_products.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add New Product'})

@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})

@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_orders.html', {'orders': orders})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        messages.success(request, f'Order #{order.id} status updated.')
    return redirect('manage_orders')

@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('manage_products')
    return render(request, 'dashboard/confirm_delete.html', {'item': product, 'type': 'product'})

@staff_member_required
def seller_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/manage_categories.html', {'categories': categories})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add New Category'})

@staff_member_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('manage_categories')
    return render(request, 'dashboard/confirm_delete.html', {'item': category, 'type': 'category'})


# Banner Management Views
@staff_member_required
def manage_banners(request):
    banners = Banner.objects.all().order_by('order', 'created_at')
    return render(request, 'dashboard/manage_banners.html', {'banners': banners})


@staff_member_required
def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner added successfully!')
            return redirect('manage_banners')
    else:
        form = BannerForm()
    return render(request, 'dashboard/banner_form.html', {
        'form': form, 
        'title': 'Add New Banner'
    })


@staff_member_required  
def edit_banner(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner updated successfully!')
            return redirect('manage_banners')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'dashboard/banner_form.html', {
        'form': form, 
        'title': f'Edit Banner: {banner.title}'
    })


@staff_member_required
def delete_banner(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, 'Banner deleted successfully.')
        return redirect('manage_banners')
    return render(request, 'dashboard/confirm_delete.html', {
        'item': banner, 
        'type': 'banner'
    })


# Profile Picture Management
@login_required
def edit_profile_pic(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('seller_dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'dashboard/profile_form.html', {
        'form': form,
        'title': 'Update Profile Picture'
    })
