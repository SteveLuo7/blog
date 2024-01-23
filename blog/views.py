from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


# Create your views here.
#   博客首页
def index(request):
    #   调用models模型类的POST方法 查询到所有发布的文章
    post_list = Post.objects.all().order_by('-add_time')
    #   创建一个分页方法
    paginator = Paginator(post_list,8)
    page_number = request.GET.get('page')
    #   下方显示分页条
    page_obj = paginator.get_page(page_number)
    #   创建上下文
    context = {"page_obj":page_obj}

    return render(request,'index.html',context)

def category_list(request, category_id):
    category = get_object_or_404(Category,id=category_id)
    posts = category.post_set.all().order_by('-add_time')
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={"category":category, "page_obj":page_obj}

    return render(request, 'list.html', context)

def post_detail(request, post_id):
    # 文章详情页
    post = get_object_or_404(Post, id=post_id)

    # 用文章id来实现的上下篇
    prev_post = Post.objects.filter(id__lt=post_id).last()  # 上一篇
    next_post = Post.objects.filter(id__gt=post_id).first()  # 下一篇
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 这个功能有漏洞，仅做思路讲解

    # 用发布日期来实现上下篇
    # date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    # date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()

    context = {'post': post, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'detail.html', context)

def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list, 8)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'index.html', context )


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    paginator = Paginator(post_list, 8)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'archives_list.html', context )
