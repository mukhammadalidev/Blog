from django.urls import path

from users.views import add_like
from .views import PostView,AuthorPostsView,AddPostView,DetailPostView,Dashboard,EditPostStatView,DeleteView,FilterBaseViewPost,MyPostView
app_name="posts"
urlpatterns = [
    path('',PostView.as_view(),name="main"),
    path('author/',AuthorPostsView.as_view(),name="author"),
    path('addpost/',AddPostView.as_view(),name="addpost"),
    path('<int:id>/detail/',DetailPostView.as_view(),name="detail"),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('edit/<int:id>/',EditPostStatView.as_view(),name="edit"),
    path('delete/<int:id>/',DeleteView.as_view(),name="delete"),
    path('filter/',FilterBaseViewPost.as_view(),name="filter"),
    path('my-post/',MyPostView.as_view(),name="my_post"),
path('add-like/<int:post_id>/', add_like, name='add_like'),
]