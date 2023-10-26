from django import forms

from blog.models import Article


class ArticleForms(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
