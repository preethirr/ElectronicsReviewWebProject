from django.db import models #type: ignore
# Create your models here.

from django.contrib.auth.models import User #type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator #type: ignore

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField(null=True)
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    category_created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    product_details = models.TextField(null=True)
    product_created_at = models.DateTimeField(auto_now_add=True, null=True)
    product_image = models.ImageField(upload_to='profile_pic/',blank=True,null=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.product_name
    
    def get_average_rating(self):
        """Calculate average rating for the product"""
        reviews = self.review_set.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0
    
    def get_rating_count(self):
        """Get total number of reviews"""
        return self.review_set.count()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'user')  # One review per user per product
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.rating}/5)"

class Newsletter(models.Model):
    email = models.EmailField(unique=True, help_text="Email address for newsletter subscription")
    is_active = models.BooleanField(default=True, help_text="Is subscription active")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
    
    def __str__(self):
        status = "Active" if self.is_active else "Unsubscribed"
        return f"{self.email} - {status}"