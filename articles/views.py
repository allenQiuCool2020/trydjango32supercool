from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import Articleform
from django.db.models import Q

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
        # return redirect('article-detail', slug=obj.slug)
        return redirect(obj.get_absolute_url())
   
    print(f"context: {context}")
    return render(request, "articles/create.html", context=context)

def article_detail_view(request, slug=None):
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404("Article does not exist")
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.get(slug=slug).first()
        except:
            raise Http404
        context = {
        "object": article_obj
    }
    return render(request, "articles/detail.html", context=context)

def article_search_view(request):
    # print(request.GET)
    # below is a dictionary
    query = request.GET['q'] 
    qs = Article.objects.search(query)
    context = {
        "object_list":qs
    }
    return render(request, "articles/search.html", context=context)

    