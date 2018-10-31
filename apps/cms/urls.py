from django.urls import path
from .views import cms_login,cms_index,CmsNews,NewsCategory,news_query,tag_delete,tag_edit,banners,upload
app_name = 'cms'
urlpatterns = [
    path('login', cms_login, name='login'),
    path('index', cms_index, name='cmsindex'),
    path('news/', CmsNews.as_view(), name='news'),
    path('newstag', NewsCategory.as_view(), name='category'),
    path('newsquery', news_query, name='newsquery'),
    path('tag_delete/<int:id>', tag_delete, name="tag_delete"),
    path("tag_edit/",tag_edit,name="tag_edit"),
    path('banner/',banners,name='banners'),
    path('upload/',upload,name='upload')
]