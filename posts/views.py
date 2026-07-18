from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from posts.forms import PostForm, PostEditForm
from posts.models import Comment, Post, Like

def home(request):
    return redirect("post_list")

class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        
        liked_post_ids = []
        if self.request.user.is_authenticated:
            liked_post_ids = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context["liked_post_ids"] = liked_post_ids
        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            Post.objects.all()
            .select_related("user")
            .prefetch_related("comments", "comments__user")
        )
        if search := self.request.GET.get("search", None):
            qs = qs.filter((Q(title_icontains=search) | Q(content_icontains=search)))
        return qs

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Post:
        if queryset is None:
            queryset = Post.objects.all()
        qs = queryset.prefetch_related("comments", "comments__user").select_related("user")
        return super().get_object(qs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        liked_post_ids = []
        if self.request.user.is_authenticated:
            liked_post_ids = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context["liked_post_ids"] = liked_post_ids
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("post_list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(
            reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})
        )

class CreateCommentGenericView(CreateView):
    model = Comment
    fields = ["content"]
    success_url = reverse_lazy("post_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = Post.objects.get(id=self.kwargs["pk"])
        form.instance.post = post
        if self.request.user.is_anonymous:
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(
            reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})
        )

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    like_filter = Like.objects.filter(user=request.user, post=post)
    if like_filter.exists():
        like_filter.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/posts/'))