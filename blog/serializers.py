from rest_framework import serializers
from .models import Article, Category

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title','status', 'body', 'views','category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']