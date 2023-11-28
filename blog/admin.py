from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article,MarkdownxModelAdmin)

