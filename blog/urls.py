from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from posts.views import about, home, post_create, post_list, toggle_like, add_comment, post_detail
from users.views import login_view, register_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("posts/", post_list, name="post_list"),
    path("posts/<int:post_id>/", post_detail, name="post_detail"),
    path("posts/create/", post_create, name="post_create"),
    path("posts/<int:post_id>/like/", toggle_like, name="toggle_like"),
    path("posts/<int:post_id>/comment/", add_comment, name="add_comment"),
    path("user/login/", login_view, name="login"),
    path("user/register/", register_view, name="register"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)