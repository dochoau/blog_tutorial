from django.contrib import admin
from .models import Post, PostView, Like, Comment, User

# Registrar los Modelos
admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(User)