from django import forms
from apps.forms import FormsMxin
from .models import Article, Banners


class TagForm(forms.Form):
    tag = forms.CharField(required=True, error_messages={'required': "添加的标签不能为空"})


class TagForm2(forms.Form):
    id = forms.IntegerField(required=True)
    tag = forms.CharField(required=True, error_messages={'required': "添加的标签不能为空"})


class ArticleForm(forms.ModelForm, FormsMxin):
    tag = forms.IntegerField()

    class Meta:
        model = Article
        exclude = ["tag", "pub_time", "author"]


class BannerForm(forms.ModelForm,FormsMxin):
    class Meta:
        model = Banners
        fields = "__all__"
