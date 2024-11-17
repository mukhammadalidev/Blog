from django.contrib import admin
from .models import Post,Author,PostReview,PostAuthor,Like
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title','created_time')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostReview)
admin.site.register(PostAuthor)
admin.site.register(Like)
