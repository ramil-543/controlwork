from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm

def home(request):
    return redirect("post_list")

def about(request):
    return render(request, "about.html")

def post_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(title__icontains=search_query)
    else:
        posts = Post.objects.all()
    
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        
    context = {
        'posts': posts,
        'count': posts.count(),
        'liked_post_ids': liked_post_ids,
    }
    return render(request, "posts/post_list.html", context)

@login_required(login_url='login')
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.rate = 5
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "posts/post_create.html", {"form": form})
@login_required(login_url='login')
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    like_filter = Like.objects.filter(user=request.user, post=post)
    
    if like_filter.exists():
        like_filter.delete()
    else:
        Like.objects.create(user=request.user, post=post)
        
    return redirect('post_list')

@login_required(login_url='login')
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment_text = request.POST.get('text', '').strip()
        if comment_text:
            Comment.objects.create(user=request.user, post=post, text=comment_text)
    return redirect('post_list')

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        
    context = {
        'post': post,
        'liked_post_ids': liked_post_ids,
    }
    return render(request, "posts/post_detail.html", context)