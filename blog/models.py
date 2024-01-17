from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string


# Create your models here.
#   博客的类别 ORM
class Category(models.Model):
    name =models.CharField(max_length=30,unique=True,verbose_name="博客类别")

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = verbose_name
        db_table = 'category_table'

    def __str__(self):
        return self.name

#   博客文章标签的ORM
class Tag(models.Model):
    name = models.CharField(max_length=30,unique=True,verbose_name="文章标签")

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name
        db_table = "tag_table"

    def __str__(self):
        return self.name

#   博客文章的ORM
class Post(models.Model):
    title = models.CharField(max_length=100,unique=True,verbose_name="文章标题")
    desc = models.TextField(max_length=200,blank=True,default="",verbose_name="文章简介")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="博客类别")
    content = models.TextField(verbose_name="文章内容")
    tags = models.ForeignKey(Tag,on_delete=models.CASCADE,verbose_name="文章标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="作者")

    is_hot = models.BooleanField(default=False,verbose_name="热门")
    pv =models.IntegerField(default=0,verbose_name="浏览量")
    add_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True,verbose_name="发布时间")

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = verbose_name
        db_table = "post_table"

    def __str__(self):
        return self.title

#   侧边栏的ORM
class Sidebar(models.Model):
    #   侧边栏展示类别
    DISPLAY_TYPE =(
        (1,"搜索"),
        (2,"联系我们"),
        (3,"最近更新"),
        (4,"热门标签"),
    )

    STATUS = [
        (1, '隐藏'),
        (2, '展示')
    ]

    title = models.CharField(max_length=60,verbose_name="侧边栏标题")
    display_type  = models.PositiveIntegerField(default=1,choices=DISPLAY_TYPE,verbose_name="侧边栏展示")
    content = models.CharField(max_length=100,blank=True,default="",verbose_name="内容",help_text="如果设置的不是HTML，可为空")
    sort = models.PositiveIntegerField(default=1,verbose_name="排序",help_text="序号越大位置越考前")
    add_date = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="状态")
    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.title

    #   类方法的装饰器，
    @classmethod
    def get_sidebar(cls):
        return cls.objects.filter(status=2)     #   查询到侧边栏所有的展示模块

    #   构建一个类属性
    @property
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('sidebar/search.html',context=context)
        elif self.display_type == 2:
            context = {

            }
            return render_to_string('sidebar/contactus.html',context=context)
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('sidebar/new_post.html', context=context)
        elif self.display_type == 4:
            context = {

            }
            return render_to_string('sidebar/hot_post.html', context=context)

        return self.content
