from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from posts.models import Like,Post
from .models import CustomerUser, Friendship
from .forms import RegisterForm, UserProfileForm, UsersProfileEditForm
from .models import CustomerUser
# Create your views here.
class LoginView(View):
    def get(self,request):
        form = AuthenticationForm()
        return render(request,'login.html',{"form":form})

    def post(self,request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)

            return redirect('/')
        else:
            return render(request, 'login.html', {"form": form})



class Register(View):
    def get(self,request):
        user_form = RegisterForm()
        return render(request,'register.html',{"form":user_form})
    def post(self,request):
        user_form = RegisterForm(data=request.POST,files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('users:login')
        else:
            return render(request, 'register.html', {"form": user_form})



class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("posts:main")


class ProfileView(View):
    def get(self,request):
        user_profile = request.user
        profile_form = UserProfileForm(instance=request.user)
        return render(request,'profile.html',{"user":user_profile,"profile":profile_form})

    def post(self,request):
        profile = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)

        if profile.is_valid():
            profile.save()
            return redirect("users:profile")
        else:
            return render(request, 'profile.html', {"user": request.user})



def send_friend_request(request, receiver_id):
    if request.user.is_authenticated:
        receiver = CustomerUser.objects.get(pk=receiver_id)
        friendship_request = Friendship(sender=request.user, receiver=receiver, status='pending')
        friendship_request.save()
    return redirect('profile')  # Redirect to the user's profile page


class UsersView(View):
    def get(self,request):
        users = CustomerUser.objects.all()
        return render(request,'users.html',{"users":users})

class UserEditView(View):
    def get(self,request,id):
        users = CustomerUser.objects.get(id=id)
        users_form = UsersProfileEditForm(instance=users)
        context = {
            "users":users,
            "form":users_form
        }

        return render(request,'user-edit.html',context)

    def post(self,request,id):
        users = CustomerUser.objects.get(id=id)
        users_form = UsersProfileEditForm(instance=users,data=request.POST,files=request.FILES)

        if users_form.is_valid():
            users_form.save()
            return redirect("users:users")
        else:
            context = {
                "users": users,
                "form": users_form
            }
            return render(request, 'user-edit.html', context)



class DeleteUserView(View):
    def get(self,request,id):
        user_db = CustomerUser.objects.get(id=id)

        user_db.delete()

        return redirect("users:users")

@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('/')