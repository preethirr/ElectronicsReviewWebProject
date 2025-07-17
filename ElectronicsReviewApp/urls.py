from django.urls import path #type: ignore
from django.conf.urls.static import static #type: ignore
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    
    # Regular user authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    
    # Admin/Superuser authentication
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('insideraccess/', views.insideraccess, name='insideraccess'),

    # General pages
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    
    # Review management (superuser only)
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    # path('shop/', views.shop, name='shop'),

    # Category management (admin only)
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:id>/update/', views.category_update, name='category_update'),
    path('category/<int:id>/delete/', views.category_delete, name='category_delete'),

    # Product management (admin only)
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:id>/update/', views.product_update, name='product_update'),
    path('product/<int:id>/delete/', views.product_delete, name='product_delete'),

    # Newsletter management
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/unsubscribe-page/', views.newsletter_unsubscribe_page, name='newsletter_unsubscribe_page'),

   
    # path('cart/', views.cart, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('detail/', views.detail, name='detail'),
    # path('contact/', views.contact, name='contact'),
    # path('about/', views.about, name='about'),
    # path('products/', views.products, name='products'),
   
   

    # path('login/', views.login_user, name='login'),
    # 
    # path('logout/', views.logout_user, name='logout'),
]