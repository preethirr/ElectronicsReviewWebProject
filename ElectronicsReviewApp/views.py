from django.shortcuts import render, redirect, get_object_or_404, redirect #type: ignore
from django.contrib.auth import authenticate, login, logout #type: ignore
from django.contrib import messages #type: ignore
from .forms import UserRegisterForm, CategoryForm, ProductForm, ContactForm, ReviewForm, NewsletterForm #type: ignore
from .models import Category, Product, Review, Newsletter #type: ignore
from django.contrib.auth.decorators import login_required, user_passes_test #type: ignore
from django.contrib.admin.views.decorators import staff_member_required #type: ignore
from django.core.mail import send_mail #type: ignore
from django.conf import settings #type: ignore
from django.utils import timezone #type: ignore
from django.db.models import Avg #type: ignore

# Create your views here.

def index(request):
    """Home page with categories and products"""
    categories = Category.objects.all()
    
    # Add product count for each category
    categories_with_counts = []
    for category in categories:
        product_count = Product.objects.filter(product_category=category).count()
        categories_with_counts.append({
            'category': category,
            'product_count': product_count
        })
    
    # Get featured products (latest products)
    featured_products = Product.objects.all().order_by('-id')[:8]
    
    # Get recent products (different from featured)
    recent_products = Product.objects.all().order_by('-id')[8:16]  # Next 8 products
    
    context = {
        'categories_with_counts': categories_with_counts,
        'featured_products': featured_products,
        'recent_products': recent_products,
    }
    return render(request, 'index.html', context)
# def index(request):
#     # return render(request,'index.html')
#     return render(request, 'index.html', {'UserName': request.user.username})



def shop(request):
    return render(request, 'index.html')

def contact(request):
    print(f"Contact view called with method: {request.method}")  # Debug line
    
    if request.method == 'POST':
        print("Processing POST request")  # Debug line
        form = ContactForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")  # Debug line
        
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            print(f"Form data - Name: {name}, Email: {email}, Subject: {subject}")  # Debug line
            
            # Compose email
            email_subject = f"Contact Form: {subject}"
            email_message = f"""
            New message from Electronics Review Contact Form:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """
            
            try:
                # Send email
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@electronicsreview.com')
                
                print("="*50)
                print("EMAIL BEING SENT:")
                print(f"Subject: {email_subject}")
                print(f"From: {from_email}")
                print(f"To: {settings.CONTACT_EMAIL}")
                print("Message:")
                print(email_message)
                print("="*50)
                
                send_mail(
                    email_subject,
                    email_message,
                    from_email,
                    [settings.CONTACT_EMAIL],  # Recipient email
                    fail_silently=False,
                )
                print("Email sent successfully!")  # Debug line
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                # Show the actual error for debugging
                messages.error(request, f'Error sending email: {str(e)}')
                print(f"Email error: {e}")  # This will show in your terminal
        else:
            print(f"Form errors: {form.errors}")  # Debug line
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def about(request):
    return render(request,'about.html')

def categories(request):
    """Display all categories with product counts"""
    categories = Category.objects.all()
    
    # Add product count for each category
    categories_with_counts = []
    for category in categories:
        product_count = Product.objects.filter(product_category=category).count()
        categories_with_counts.append({
            'category': category,
            'product_count': product_count
        })
    
    context = {
        'categories_with_counts': categories_with_counts,
    }
    return render(request, 'categories_page.html', context)

def category_detail(request, id):
    """Display all products in a specific category"""
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(product_category=category)
    
    context = {
        'category': category,
        'products': products,
        'product_count': products.count(),
    }
    return render(request, 'category_detail.html', context)

# def view_cart(request):
#     return render(request,'cart.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                print(f"User {username} authenticated successfully, redirecting to index")  # Debug line
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
                print(f"Authentication failed for user: {username}")  # Debug line
        else:
            messages.error(request, 'Please fill in both username and password.')
            print("Missing username or password")  # Debug line
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')

def signup_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def admin_login(request):
    """Separate login for admin/superuser access"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome Admin {user.username}!')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Access denied. Admin privileges required.')
            else:
                messages.error(request, 'Invalid admin credentials.')
        else:
            messages.error(request, 'Please fill in both username and password.')
    return render(request, 'admin_login.html')

def is_admin(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    """Admin dashboard - only accessible to staff/superuser"""
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    recent_products = Product.objects.all().order_by('-id')[:5]
    categories = Category.objects.all()[:5]  # Get some categories for display
    
    # Newsletter statistics - with debugging
    all_newsletters = Newsletter.objects.all()
    active_newsletters = Newsletter.objects.filter(is_active=True)
    total_newsletter_subscribers = active_newsletters.count()
    total_newsletter_unsubscribed = Newsletter.objects.filter(is_active=False).count()
    recent_newsletter_subscribers = active_newsletters.order_by('-subscribed_at')[:10]
    
    # Debug print to console
    print(f"DEBUG: Total newsletters in DB: {all_newsletters.count()}")
    print(f"DEBUG: Active newsletters: {total_newsletter_subscribers}")
    print(f"DEBUG: Inactive newsletters: {total_newsletter_unsubscribed}")
    
    # Review statistics
    total_reviews = Review.objects.count()
    recent_reviews = Review.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_products': recent_products,
        'categories': categories,
        'total_newsletter_subscribers': total_newsletter_subscribers,
        'total_newsletter_unsubscribed': total_newsletter_unsubscribed,
        'recent_newsletter_subscribers': recent_newsletter_subscribers,
        'total_reviews': total_reviews,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def insideraccess(request):
    """Enhanced insider access with proper authentication"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_login')
    
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'user': request.user
    }
    return render(request,'insideraccess.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'product_add_edit.html', {'form': form})

def product_update(request,id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_add_edit.html', {'form': form})

def product_delete(request,id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    return render(request, 'product_delete.html', {'product': product})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CategoryForm()
    return render(request, 'category_add_edit.html', {'form': form})

def category_update(request,id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_add_edit.html', {'form': form})

def category_delete(request,id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_dashboard')
    return render(request, 'category_delete.html', {'category': category})


def product_detail(request, id):
    """Product detail page with reviews and rating functionality"""
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    # Handle review form submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to write a review.')
            return redirect('login')
        
        if user_review:
            messages.error(request, 'You have already reviewed this product.')
            return redirect('product_detail', id=id)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product_detail', id=id)
    else:
        form = ReviewForm()
    
    # Calculate average rating and rating distribution
    average_rating = product.get_average_rating()
    rating_count = product.get_rating_count()
    
    # Rating distribution for display
    rating_distribution = {i: 0 for i in range(1, 6)}
    for review in reviews:
        rating_distribution[review.rating] += 1
    
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'average_rating': average_rating,
        'rating_count': rating_count,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'product_detail.html', context)


@login_required
def edit_review(request, review_id):
    """Edit review - only superusers can edit reviews"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only superusers can edit reviews
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit reviews.')
        return redirect('product_detail', id=review.product.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('product_detail', id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'product': review.product,
    }
    return render(request, 'edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """Delete review - only superusers can delete reviews"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only superusers can delete reviews
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete reviews.')
        return redirect('product_detail', id=review.product.id)
    
    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('product_detail', id=product_id)
    
    context = {
        'review': review,
        'product': review.product,
    }
    return render(request, 'delete_review.html', context)

def products(request):
    """Display all products with filtering, search and sorting"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            product_name__icontains=search_query
        ).union(
            products.filter(product_details__icontains=search_query)
        ).union(
            products.filter(product_category__category_name__icontains=search_query)
        )
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(product_category_id=category_id)
    
    # Handle sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'name':
        products = products.order_by('product_name')
    elif sort_by == 'price-low':
        products = products.order_by('product_price')
    elif sort_by == 'price-high':
        products = products.order_by('-product_price')
    elif sort_by == 'rating-high':
        # Sort by average rating (highest first)
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating', '-id')
    elif sort_by == 'rating-low':
        # Sort by average rating (lowest first)
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('avg_rating', 'id')
    elif sort_by == 'newest':
        products = products.order_by('-product_created_at')
    elif sort_by == 'oldest':
        products = products.order_by('product_created_at')
    else:
        products = products.order_by('-product_created_at')  # Default: newest first
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'current_sort': sort_by,
        'search_query': search_query,
    }
    return render(request, 'products.html', context)

def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save()
            
            # Send welcome email
            try:
                subject = "Welcome to Electronics Review Newsletter!"
                message = f"""
                Dear Subscriber,

                Thank you for subscribing to the Electronics Review newsletter!
                
                You'll now receive the latest updates about:
                • New product reviews and ratings
                • Tech news and trends
                • Special offers and deals
                • Product recommendations

                Email: {newsletter.email}
                Subscribed on: {newsletter.subscribed_at.strftime('%B %d, %Y')}

                If you didn't subscribe to this newsletter, you can unsubscribe at any time.

                Best regards,
                Electronics Review Team
                """
                
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@electronicsreview.com')
                send_mail(
                    subject,
                    message,
                    from_email,
                    [newsletter.email],
                    fail_silently=True,
                )
                
                messages.success(request, f'Successfully subscribed {newsletter.email} to our newsletter!')
            except Exception as e:
                messages.success(request, f'Successfully subscribed to our newsletter! (Welcome email delivery pending)')
            
            # Redirect to prevent duplicate submission
            return redirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            # Extract the error message
            if 'email' in form.errors:
                error_msg = form.errors['email'][0]
                messages.error(request, error_msg)
            else:
                messages.error(request, 'Please enter a valid email address.')
    
    # Redirect back to the page where the form was submitted
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def newsletter_unsubscribe(request):
    """Handle newsletter unsubscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                newsletter = Newsletter.objects.get(email=email, is_active=True)
                newsletter.is_active = False
                newsletter.unsubscribed_at = timezone.now()
                newsletter.save()
                messages.success(request, f'Successfully unsubscribed {email} from our newsletter.')
            except Newsletter.DoesNotExist:
                messages.error(request, 'Email address not found in our newsletter list.')
        else:
            messages.error(request, 'Please provide an email address.')
    
    return redirect('index')

def newsletter_unsubscribe_page(request):
    """Display the newsletter unsubscribe page"""
    return render(request, 'newsletter_unsubscribe.html')