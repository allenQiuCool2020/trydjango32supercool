from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm,RecipeIngredientForm
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404
from django.urls import reverse
# CRUD -> Create Retrieve Update and Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context=context)

@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs= {"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context)


@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found")
    context = {
        "object": obj
    }
    return render(request,"recipes/partials/detail.html", context)

@login_required
def recipe_delete_view(request, id=None):
    try:
        obj = get_object_or_404(Recipe, id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("not found")
    if request.method == 'POST':
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse("ok", headers=headers)
        return redirect(success_url)
    context = {
        "object": obj,
    }
    return render(request,"recipes/delete.html", context)

@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = get_object_or_404(RecipeIngredient, recipe__id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("not found")
        raise Http404
    if request.method == 'POST':
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={"id": parent_id})
        if request.htmx:
            context = {
                "name": obj.name
            }
            return render(request, "recipes/partials/ingredient-inline-delete-response.html", context=context)
        return redirect(success_url)
    context = {
        "object": obj,
    }
    return render(request,"recipes/delete.html", context)

@login_required
def recipe_create_view(request, id=None):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context=context)

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs= {"parent_id": id})
    context = {
        "object": obj,
        "form": form,
        "new_ingredient_url": new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'
    if request.htmx:
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create-update.html", context=context)

@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Recipe Not Found")
    
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    
    url = reverse("recipes:hx-ingredient-create", kwargs= {"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form":form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request,"recipes/partials/ingredient-inline.html", context)
    
    return render(request,"recipes/partials/ingredient-form.html", context)
