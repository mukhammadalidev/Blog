from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from hitcount.views import DetailView, HitCountMixin
from posts.forms import AddPostForm, AddComment, DashboardForm, EditUserPost
from posts.models import Post, PB, Author, PostAuthor, PostReview, DR


# Create your views here.

class PostView(View):
    def get(self,request):
        posts = Post.objects.filter(status=PB)
        search_query = request.GET.get('q')
        if search_query:
            posts = posts.filter(title__icontains=search_query)
        context = {
            "posts":posts
        }
        return render(request,'home.html',context)

class AuthorPostsView(View):
    def get(self,request):
        author = PostAuthor.objects.all()
        user = Author.objects.all()


        context = {
            "author":author,"user":user
        }

        return render(request,'author.html',context)

class AddPostView(View):
    def get(self,request):

        add_form = AddPostForm()
        context = {
            "form":add_form
        }
        return render(request,'add.html',context)
    def post(self,request):
        user = request.user
        add_form = AddPostForm(data=request.POST,files=request.FILES)

        if add_form.is_valid():
            post = add_form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("posts:main")
        else:
            context = {
                "form": add_form
            }
            return render(request, 'add.html', context)


class DetailPostView(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        comment = AddComment()
        contex = {}
        hit_count = HitCount.objects.get_for_object(post)
        hits = hit_count.hits
        contex['hitcount'] = {"pk": hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)

        if hit_count_response.hit_counted:
            hits += 1
            contex['hit_counted'] = hit_count_response.hit_counted
            contex['hit_message'] = hit_count_response.hit_message
            contex['total_hits'] = hits

        context = {
            "post":post,
            "comment":comment,
            "hit_count_response": hit_count_response
        }
        return render(request,'detail-post.html',context)

    def post(self,request,id):
        post = Post.objects.get(id=id)
        review_form = AddComment(data=request.POST)

        if review_form.is_valid():
            PostReview.objects.create(
                post=post,
                author=request.user,
                comment=review_form.cleaned_data['comment'],
                review = review_form.cleaned_data['review']
            )
            return redirect(reverse("posts:detail",kwargs={"id":post.id}))
        else:
            context = {
                "post": post
            }
            return render(request, 'detail-post.html', context)





class Dashboard(View):
    def get(self,request):
        posts = Post.objects.all().order_by('-created_time')
        context = {
            "posts":posts
        }
        return render(request,'dashboard.html',context)

# class DashboardStatusEdit(View):
#     def post(self,request,id):
#         posts = Post.objects.get(id=id)
#         status_form = DashboardForm(data=request.POST)

class EditPostStatView(View):
    def get(self,request,id):
        post_db = Post.objects.get(id=id)
        if request.user.is_superuser:
            post_form = DashboardForm(instance=post_db)
        else:
            post_form = EditUserPost(instance=post_db)

        return render(request,'edit.html',{"form":post_form})

    def post(self,request,id):

        post_db = Post.objects.get(id=id)
        if request.user.is_superuser:
            post_form = DashboardForm(instance=post_db,data=request.POST,files=request.FILES)
        else:
            post_form = EditUserPost(instance=post_db)
        if post_form.is_valid():
            post_form.save()
            return redirect("posts:dashboard")
        else:
            return render(request, 'edit.html', {"form": post_form})



class DeleteView(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        post.delete()
        return redirect("posts:dashboard")



class FilterBaseViewPost(View):

    def get(self,request):
        isSelect = ''
        recommended_posts = Post.objects.filter(status=PB)

        from datetime import timedelta

        filter = request.GET.get('filter',request.GET.get('filter'))
        print(filter)
        if filter == 'hours':
            time_threshold = timezone.now() - timedelta(hours=1)
            recommended_posts = recommended_posts.filter(created_time__gte=time_threshold)
            isSelect = 'hours'
            context = {
                "recomment_post": recommended_posts,
                "select":isSelect

            }
            return render(request, 'main.html', context)
        elif filter == 'week':
            time_threshold = timezone.now() - timedelta(days=7)
            recommended_posts = recommended_posts.filter(created_time__gte=time_threshold)
            isSelect = 'week'
            context = {
                "recomment_post": recommended_posts,
                "select": isSelect

            }
            return render(request, 'main.html', context)
        elif filter == 'year':
            time_threshold = timezone.now() - timedelta(days=365)
            recommended_posts = recommended_posts.filter(created_time__gte=time_threshold)
            isSelect = 'year'
            context = {
                "recomment_post": recommended_posts,
                "select": isSelect

            }
            return render(request, 'main.html', context)
        else:
            context = {
                "recomment_post": recommended_posts,
                "select":isSelect

            }
            return render(request,'main.html',context)



class MyPostView(View):
    def get(self,request):
        posts = Post.objects.filter(author=request.user).order_by("id")
        search_query = request.GET.get('q')
        if search_query:
            posts = posts.filter(title__icontains=search_query)
        paginator = Paginator(posts,15)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)
        return render(request,'my_post.html',{"posts":page_obj})
