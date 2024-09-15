from apps.blog.models import Categories

def categories_processor(request):
    categories = Categories.objects.all().order_by('-id')
    return {'categories': categories}