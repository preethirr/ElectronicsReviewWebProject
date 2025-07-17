from .models import Category

def categories_context(request):
    """
    Context processor to make categories and search query available in all templates
    """
    categories = Category.objects.all()
    search_query = request.GET.get('search', '')
    return {
        'navbar_categories': categories,
        'search_query': search_query
    }
