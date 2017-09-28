from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown

# Create your models here.
# python_2_unicode_compatible 装饰器用于兼容python2
@python_2_unicode_compatible
class Category(models.Model):
    """
    django要求模型必须继承models.Model类。
    CharField指定了分类名name的数据类型，CharField是字符型
    max_length指定最大长度，超过此长度的分类名不能存储到数据库
    """
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签Tag,和Category一样
    一定要继承models.Model类!
    """
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name 


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章的数据库表比较复杂一点，涉及的字段更多
    """


    """文章标题"""
    title = models.CharField(max_length=70)

    """
    文章正文，我们使用了TextField
    存储比较短的字符串可以使用CharField,但对于文章的正文来说可能会是一大段文本，因此使用TextField来存储打文本 
    """
    body = models.TextField()

    """
    下面两个列分别表示文章的创建时间和最后一次修改时间，存储时间用DateTimeField类型
    """
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    """
    文章摘要，可以没有，默认情况下CharField要求我们必须存入数据，否则就会报错
    指定CharFiled的blank=True参数值后就可以允许空值了。
    """
    excerpt = models.CharField(max_length=200, blank=True)
    

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 先实例化一个Markdown类，用于渲染body文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])

            # 先将Markdown文本渲染成HTML文本
            # strip_tags方法去掉HTML文本中全部的HTML标签
            # 从文本中摘取前54个字符赋给excerpt
            self.excerpt = strip_tags(md.convert(self.body)[:54])
        # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    """
    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对象的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是ForeignKey（一对多）
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可以有多篇文章，所以使用ManyToManyField（多对多）
    # 可以运行文章没有标签，因此为标签tags指定了blank=Ture
    """
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    """
    # 文章作者，这里的User是从django.contrib.auth.models导入的
    # django.contrib.auth是Django内置的应用，专门用于处理网站用户的注册、登录等流程，User是Django为我们写好的用户模型
    # 一篇文章只能有一个作者，一个User可能有多篇文章，这里用ForeignKey将User和文章关联起来
    """
    author = models.ForeignKey(User)


    # 新增views字段统计阅读量
    views = models.PositiveIntegerField(default=0)


    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})


    class Meta:
        ordering = ['-create_time', 'title']
