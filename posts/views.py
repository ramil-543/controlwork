from django.shortcuts import render
from posts.models import Post

def home(request):
   
    return render(request, 'index.html', {'posts': []})

def about(request):
   
    return render(request, 'index.html', {'posts': []})

def post_list(request):
  
    posts = Post.objects.filter(is_published=True)
    return render(request, 'index.html', {'posts': posts})