from typing import Any
from django import forms
from .models import Article
class Articleform(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self) -> dict[str, Any]:
        data = self.cleaned_data
        title = data['title']
        qs = Article.objects.all().filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f"\"{title}\" had been taken")
        return data
    
class ArticleformOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean_title(self):
        cleaned_data = self.cleaned_data
        print(f"clearned data: {cleaned_data}")
        title = cleaned_data['title']
        print(f"title: {title}")
        return title