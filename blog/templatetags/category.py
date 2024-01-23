from django import template

from blog.models import Category, Sidebar, Post

register = template.Library()

@register.simple_tag
def get_category_list():
    #获取博客分类的方法 在category这里注册 供前端调用
    return Category.objects.all()

@register.simple_tag
def get_sidebar_list():
    #侧边栏方法
    return Sidebar.objects.all()

@register.simple_tag
def get_new_post():
    #   最近更新
    return Post.objects.order_by('-add_time')[:5]

@register.simple_tag
def get_hot_post():
    # 手动热门推荐
    return Post.objects.filter(is_hot=True)[:5]

@register.simple_tag
def get_hot_pv_post():
    # 手动热门推荐
    return Post.objects.order_by('-pv')[:5]

@register.simple_tag
def get_archives():
    # 文章归档
    return Post.objects.dates('add_date', 'month', order='DESC')[:5]





