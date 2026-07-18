from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from posts.views import (
    home, 
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView, 
    CreateCommentGenericView, 
    DeletePostView, 
    toggle_like
)
from users.views import login_view, register_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", DeletePostView.as_view(), name="post_delete"),
    path("posts/<int:pk>/comment/", CreateCommentGenericView.as_view(), name="add_comment"),
    path("posts/<int:post_id>/like/", toggle_like, name="toggle_like"),
    
    path("user/login/", login_view, name="login"),
    path("user/register/", register_view, name="register"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)