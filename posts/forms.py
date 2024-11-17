from django import forms
from .models import PostAuthor, Post, PostReview


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','description','post_picture',)


class AddComment(forms.ModelForm):
    review = forms.IntegerField(min_value=1,max_value=5)
    class Meta:
        model = PostReview
        fields = ('review','comment',)

class DashboardForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('__all__')



class EditUserPost(forms.ModelForm):


    class Meta:
        model = Post
        fields = ('title','description','post_picture',)


