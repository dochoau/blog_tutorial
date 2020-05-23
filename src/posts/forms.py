from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('__all__')


class CommentForm(forms.ModelForm):
    # Customizar el formulario que se muestra, se hace obligatorio antes de undir el botón
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows': 4
    }))

    class Meta:
        model = Comment
        fields = ('content',)
