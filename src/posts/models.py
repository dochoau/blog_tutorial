from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


# Este usuario hereda los campos de la clase user
class User(AbstractUser):
    # Puedo añadirle los campos que quiera
    pass

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField()
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # campo usado para hacer la busqueda desde la url
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # se especifica el nombre de la url y la variable que se le va a pasar
        return reverse("detail", kwargs={
            'slug': self.slug
        })

    def get_like_url(self):
        # se especifica el nombre de la url y la variable que se le va a pasar
        return reverse("like", kwargs={
            'slug': self.slug
        })

    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def get_comment_count(self):
        # Con este método contamos el número de comentarios que tiene el post
        # se usa comment_set, porque post es una clave foranea de comment
        return self.comment_set.all().count()

    @property
    def get_view_count(self):
        # Con este método contamos el número de comentarios que tiene el post
        # se usa comment_set, porque post es una clave foranea de comment
        return self.postview_set.all().count()

    @property
    def get_like_count(self):
        # Con este método contamos el número de comentarios que tiene el post
        # se usa comment_set, porque post es una clave foranea de comment
        return self.like_set.all().count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
