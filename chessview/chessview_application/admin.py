from django.contrib import admin
from .models import News, Lessons, Debuts, Articles, Comment

class NewsAdmin(admin.ModelAdmin):
    pass

class LessonsAdmin(admin.ModelAdmin):
    pass

class DebutsAdmin(admin.ModelAdmin):
    pass

class ArticlesAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(News, NewsAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Debuts, DebutsAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Comment, CommentAdmin)