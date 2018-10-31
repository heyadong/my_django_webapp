from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.http import require_POST
from django.views import View
from .models import NewsTag, Article
from .forms import TagForm, TagForm2, ArticleForm,BannerForm
from utils import restiful
from django.conf import settings
import os
User = get_user_model()


# def uplaodfile(file):
#     filename = os.path.join(settings.MEDIA_URL, file.name)
#     try:
#         with open(filename, 'wb') as file_obj:
#             for chunk in file.chunks():
#                 file_obj.write(chunk)
#     except Exception as e:
#         print(e)


def uplaod(request):
    form = BannerForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return restiful.success()
    else:
        return restiful.paramserror(message=form.get_errors())


def cms_login(request):
    return render(request, 'CMS/cms_login.html')


def cms_index(request):
    return render(request, 'CMS/cms_index.html')


def news_query(request):
    return render(request, 'CMS/cms_newsquery.html')


class CmsNews(View):
    def get(self, request):
        tags = NewsTag.objects.all()
        context = {
            "tags": tags
        }
        return render(request, 'CMS/cms_article.html', context=context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            thumbnail = data.get('thumbnail')
            tag = data.get("tag")
            categoryTag = NewsTag.objects.get(pk=tag)
            content = data.get('content')
            # 登陆功能出翔bug 暂时指定发布作者
            # author = request.user
            author = User.object.get(pk='Bx9BnppGDx4gwqjwQ8rLvD')
            print(author)
            print(thumbnail)
            print(title, description, thumbnail, tag, content)
            try:
                Article.objects.create(title=title,
                                       thumbnail=thumbnail,
                                       description=description,
                                       tag=categoryTag,
                                       content=content,
                                       author=author)
                return restiful.success()
            except:
                return restiful.paramserror(message="参数错误")
        else:
            return restiful.paramserror(data=form.get_errors())


class NewsCategory(View):
    # 新闻分类添加
    def get(self, request):
        tags = NewsTag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, 'CMS/cms_newstag.html', context=context)

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('tag')
            exist_tags = NewsTag.objects.filter(name=name)
            if exist_tags:
                return restiful.paramserror(message="标签已经存在")
            tag = NewsTag(name=name)
            tag.save()
            return redirect(reverse("cms:category"))
        else:
            return restiful.paramserror(message='参数错误')


def tag_delete(request, id):
    # 新闻分类删除
    if id:
        tag = NewsTag.objects.get(id=id)
        tag.delete()
        return restiful.success(message="删除标签成功")
    else:

        return restiful.paramserror(message="删除的标签不存在")


@require_POST
def tag_edit(request):
    # 新闻分类编辑
    form = TagForm2(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        tag_name = data.get('tag')
        tag_id = data.get('id')
        try:
            tag = NewsTag.objects.get(id=tag_id)
            tag.name = tag_name
            tag.save()
            return restiful.success()
        except:
            return restiful.paramserror("编辑的的标签不存在")


def banners(request):
    # 轮播图页面
    return render(request, 'CMS/cms_banners.html')

@require_POST
def upload(request):
    """
  上传文件到本地
    """
    file = request.FILES.get('file')
    print(request.FILES)
    # try:
    with open(os.path.join(settings.MEDIA_ROOT,file.name),'wb') as file_obj:
        for chunk in file.chunks():
            file_obj.write(chunk)
    # file_url = request.SERVER_NAME+':'+request.SERVER_PORT+'/'+file.name
    file_url = 'http://' + request.get_host()+'/media/'+file.name
    print(file_url)
    return restiful.success(message="上传文件成功",data={'file_url': file_url})
    # except:
    #     return restiful.paramserror(message="参数错误")


