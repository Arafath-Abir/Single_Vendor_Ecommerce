from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Authentication URLs
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Product and category URLs
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/rate/<int:product_id>/', views.rate_product, name='rate_product'),

    # Cart and others URLs
    path('Cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # checkout and payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/fail/<int:order_id>/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),

    # profile related url
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # seller dashboard
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/products/', views.manage_products, name='manage_products'),
    path('dashboard/product/add/', views.add_product, name='add_product'),
    path('dashboard/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('dashboard/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('dashboard/orders/', views.manage_orders, name='manage_orders'),
    path('dashboard/order/seller/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),
    path('dashboard/order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('dashboard/categories/', views.manage_categories, name='manage_categories'),
    path('dashboard/category/add/', views.add_category, name='add_category'),
    path('dashboard/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('dashboard/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # Banner management
    path('dashboard/banners/', views.manage_banners, name='manage_banners'),
    path('dashboard/banners/add/', views.add_banner, name='add_banner'),
    path('dashboard/banners/edit/<int:pk>/', views.edit_banner, name='edit_banner'),
    path('dashboard/banners/delete/<int:pk>/', views.delete_banner, name='delete_banner'),
    
    # Profile picture
    path('dashboard/profile-pic/', views.edit_profile_pic, name='edit_profile_pic'),
]


# media files setup for dynamic image urls
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)