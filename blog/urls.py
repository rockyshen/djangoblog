from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('articles',views.ArticleViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
