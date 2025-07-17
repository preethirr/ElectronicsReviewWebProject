from django.contrib import admin #type: ignore
from .models import Category, Product, Review, Newsletter

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_created_at']
    search_fields = ['category_name']
    list_filter = ['category_created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'product_category', 'product_created_at']
    search_fields = ['product_name', 'product_category__category_name']
    list_filter = ['product_category', 'product_created_at']
    list_editable = ['product_price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    search_fields = ['product__product_name', 'user__username']
    list_filter = ['rating', 'created_at', 'product__product_category']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
    search_fields = ['email']
    list_filter = ['is_active', 'subscribed_at']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    list_editable = ['is_active']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')
