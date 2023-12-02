from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from mdeditor.fields import MDTextField
from django.conf import settings
from blog.validators import validate_file_size

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)
    index = models.IntegerField(default=0)       # 这个字段是干什么的？

    class Meta:
        ordering = ['-index']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.title


class Article(models.Model):
    STATUS_CHOICES = (
        ('d','Draft'),
        ('p','Published'),
    )

    COMMENT_STATUS_CHOICES = (
        ('o','Open'),
        ('c','Close'),
    )

    TYPE = (
        ('a','Article'),
        ('p','Page'),
    )

    title = models.CharField(max_length=255, unique=True)
    body = MDTextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    # comment_status = models.CharField(max_length=1, choices=COMMENT_STATUS_CHOICES)
    type = models.CharField(max_length=1, choices=TYPE)
    views = models.PositiveIntegerField(default=0)      # 在views.py的def retrieve函数中调用！
    article_order = models.IntegerField(default=0)    # 重写逻辑，+=1
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)    # 当AUTH_USER_MODEL中的用户被删除时，与之关联的作者也删除
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    cover_img = models.ImageField(null=True, upload_to='blog/cover', validators=[validate_file_size])

    class Meta:
        ordering = ['-article_order','-pub_time']
        verbose_name = '文章'                       # admin管理界面时显示，改为中文
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
    
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.article_order:
            # 如果 article_order 字段没有值，为其生成一个适当的值
            max_order = Article.objects.aggregate(models.Max('article_order'))['article_order__max']
            if max_order is not None:
                self.article_order = max_order + 1
            else:
                self.article_order = 1
        super().save(*args, **kwargs)
