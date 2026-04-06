from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Cart, CartItem, Category, Order, OrderItem, Product, Rating

admin.site.unregister(User)
admin.site.unregister(Group)
try:
    admin.site.unregister(Site)
except:
    pass
try:
    admin.site.unregister(EmailAddress)
except:
    pass
try:
    admin.site.unregister(SocialAccount)
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialToken)
except:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Site)
class SiteAdmin(ModelAdmin):
    list_display = ("domain", "name")
    search_fields = ("domain", "name")

@admin.register(EmailAddress)
class EmailAddressAdmin(ModelAdmin):
    list_display = ("email", "user", "primary", "verified")
    search_fields = ("email", "user__username")

@admin.register(SocialAccount)
class SocialAccountAdmin(ModelAdmin):
    list_display = ("user", "provider")

@admin.register(SocialApp)
class SocialAppAdmin(ModelAdmin):
    list_display = ("name", "provider")

@admin.register(SocialToken)
class SocialTokenAdmin(ModelAdmin):
    list_display = ("app", "account")

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    search_fields = ["name", "description"]
    list_display = ["name", "category", "price", "stock", "available", "created_at"]
    list_filter = ["available", "category", "created_at"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter_submit = True

@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = ["product", "user", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["user__username", "product__name"]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "user", "get_total_cost", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "id", "status"]
    date_hierarchy = "created_at"

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ["order", "product", "price", "quantity"]
    search_fields = ["order__id", "product__name"]

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["id", "user", "created_at"]
    search_fields = ["user__username"]

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ["cart", "product", "quantity"]
    search_fields = ["product__name"]