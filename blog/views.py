from django.shortcuts import render
from .models import Article, Category
from rest_framework.viewsets import ModelViewSet
from blog.serializers import ArticleSerializer
from rest_framework.response import Response

# Create your views here.
# def queryall(request):
#     articlelist = Article.objects.all
#     return render(request,'index.html',{'articlelist':articlelist})

# 将上面的函数视图，修改为ViewSet
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # 重写list方法，返回值从“serializer.data“改为render渲染到模版中，并通过字典传递serializer.data
    def list(self,request, *arg, **kwarg):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # 获取所有 Category 数据
        categories = Category.objects.all()

        # 将 Article 数据和 Category 标题传递给模板
        context = {
            'articles': serializer.data,
            'categories': categories,
        }
        return render(request, 'index.html', context)