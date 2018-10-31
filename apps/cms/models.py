from django.db import models

# Create your models here.


class NewsTag(models.Model):
    name = models.CharField(max_length=50,null=False)
    add_time = models.DateField(auto_now=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=800)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey('NewsTag',on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey("authdemo.User", on_delete=models.CASCADE)


class Banners(models.Model):
    bannersimg = models.ImageField(upload_to='%Y%m%d')
    link_to = models.URLField(null=True)
    postion = models.IntegerField()
    add_time = models.DateField(auto_now_add=True)



