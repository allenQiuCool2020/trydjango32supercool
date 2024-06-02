from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import Articleform

def home_view(request, *args, **kwargs):
    article_obj = Article.objects.get(id=2)
    article_title = article_obj.title
    article_content = article_obj.content
    article_list = Article.objects.all()
    context = {
        "title": article_title,
        "id": article_obj.id,
        "content": article_content,
        "object_list": article_list
    }
    return render(request,"home-view.html", context)

@login_required
def article_create_view(request):
    form = Articleform(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save()
        context['form'] = Articleform()
   
    print(f"context: {context}")
    return render(request, "articles/create.html", context=context)

def article_detail_view(request, id):
    try:
        article_obj = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    context = {
        "object": article_obj
    }
    return render(request, "articles/detail.html", context=context)

def article_search_view(request):
    # print(request.GET)
    # below is a dictionary
    query_dict = request.GET

    try:
        query = int(query_dict['q'])
    except:
        query = None
        article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {
        "object": article_obj
    }
    return render(request, "articles/search.html", context=context)

    