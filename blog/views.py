from django import views
from django.shortcuts import get_object_or_404, render


from .models import Post, comment
from.forms import Commentform
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def starting_page(request):
    # -becacuse we want to order on latest post first
    latest_posts = Post.objects.all().order_by("-date")[:3]
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_post = sorted_posts[-3:]
    return render(request, 'blog/index.html', {
        "posts": latest_posts
    })


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, 'blog/all-posts.html', {
        "all_posts": all_posts
    })


class SinglePostView(View):
    # template_name = "blog/post-detail.html"
    # model = Post
    def is_stored_post(self,request,post_id):
        stored_posts =request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
             is_saved_for_later= False
        return is_saved_for_later
    
    def get(self,request,slug):
        post = Post.objects.get(slug =slug)
        
        context={
        "post": post,
        "post_tags": post.tags.all(),
        "comment_forms":Commentform(),
        "comments": post.comments.all().order_by("-id"),
        "saved_for_later": self.is_stored_post(request,post.id)
        }
        return render(request,"blog/post-detail.html",context)
        
    def post(self,request,slug):
        Comment_form = Commentform(request.POST)
        post = Post.objects.get(slug =slug)
        
        if Comment_form.is_valid():
            comment = Comment_form.save(commit=False)
            comment.post= post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail",args=[slug]))
        
        context={
        "post": post,
        "post_tags": post.tags.all(),
        "comment_forms":Commentform(),
        "comments": post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)
# def post_detail(request, slug):
#     indentified_post = get_object_or_404(Post,slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         "post": indentified_post,
#         "post_tags": indentified_post.tags.all(),
#         "comment_forms":Commentform()
#     })

class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        
        if  stored_posts is None:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request,"blog/stored-posts.html",context)
            
    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
            
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:
          stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts
            
        return HttpResponseRedirect("/")
            
