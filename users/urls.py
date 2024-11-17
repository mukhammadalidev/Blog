from django.urls import path
from .views import LoginView,Register,LogoutView,ProfileView,send_friend_request,UsersView,UserEditView,DeleteUserView
app_name="users"
urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path('register/', Register.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('send_request/<int:receiver_id>/',send_friend_request,name="send_friend_request"),
    path('users/',UsersView.as_view(),name="users"),
    path('users/<int:id>/',UserEditView.as_view(),name="users_edit"),
    path('users/delete/<int:id>/',DeleteUserView.as_view(),name="delete_user")

    ]