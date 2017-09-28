from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comments
from .forms import CommentsForms

# Create your views here.

def comment_post(request, post_pk):
    #先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    #这里使用get_object_or_404方法来确定文章是否存在，不存在则返回一个404页面给用户
    post = get_object_or_404(Post, pk=post_pk)

    #HTTP请求分文post和get，一般表单提交都是post请求
    #所以只有获取到了post请求时才处理表单数据
    if request.method == "POST":
        #用户提交的表单数据存在request.POST里，这是一个类字典对象
        #我们利用这些数据构造CommentsForms实例，这样Django表单就生成了
        form = CommentsForms(request.POST)
        
        #当调用form.is_valid()方法的时候django自动帮我们判断数据是否符合表单格式要求
        if form.is_valid():
            #检查到数据是合法的，调用save方法讲数据保存到数据库中
            # commit=False的作用是仅仅利用表单的数据生成comment模型类的实例，但还不保存评论到数据库
            comment = form.save(commit=False)
            
            #将评论和文章关联起来
            comment.post = post

            #最后将数据保存到数据库，调用模型实例的save方法
            comment.save()

    # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
    # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comments_set.all()
            context = {'post': post, 
                       'form': form, 
                       'coment_list': comment_list
                      }
            render(request, 'blog/detail.html', context=context)
    return redirect(post)

