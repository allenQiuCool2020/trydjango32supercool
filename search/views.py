from django.shortcuts import render
from articles.models import Article
from recipes.models import Recipe
# Create your views here.
SEARCH_TYPE_MAPPING = {
    "recipes": Recipe,
    "recipe": Recipe,
    "articles": Article,
    "article": Article
}
def search_view(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    Klass = Recipe
    if search_type in SEARCH_TYPE_MAPPING.keys():
        Klass = SEARCH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search(query=query)
    context = {
        "queryset": qs,
    }
    template = "search/results-view.html"

    if request.htmx:
        context['queryset'] = qs[:5]
        template = "search/partials/results.html"
    return render(request, template, context)