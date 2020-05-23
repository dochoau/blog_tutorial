from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostView, Like, Comment, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, CommentForm

# La clase generic ya tiene templates definidos, con el nombre del modelo y de la url, tienen que estar en una carpeta con el nombre de la api


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post

    def get_object(self, **kwargs):
        """Devuelve el objeto que la página está mostrando """
        object = super().get_object(**kwargs)
        # con el método get or create sólo lo creamos una vez
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                author=self.request.user, post=object)
        return object

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            # cómo arriba sólo recibí el comentario, me toca crear el resto y primero hacer el instance
            comment = form.instance
            comment.author = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail", slug=post.slug)
        return redirect("detail", slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        return context


class PostCreateView(CreateView):
    # El archivo html de este se debe llamar post_form
    # El create y el update van para el mismo archivo html
    form_class = PostForm
    model = Post
    # Hay que especificar el redirect
    success_url = '/'
    # Creamos el contexto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "view_type": "Crear"
        })
        return context


class PostUpdateView(UpdateView):
    # Estos son los campos que podemos actualizar
    # El archivo html de este se debe llamar post_form
    form_class = PostForm
    model = Post
    # Especificamos el Redirect
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "view_type": "Actualizar"
        })
        return context


class PostDeleteView(DeleteView):
    # el html de este se debe llamar post_confirm_delete
    model = Post
    # Hay que ponerle una succes_view, o sea donde va después de hacer el borrado, hacer el redirect
    success_url = '/'


def like(request, slug):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(author=request.user, post=post)
        if like_qs.exists():
            # si ya está el like se le quita, sino se crea
            like_qs[0].delete()
        else:
            Like.objects.create(author=request.user, post=post)
    return redirect('detail', slug=slug)
