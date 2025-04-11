from django.urls import path

from blog.views import BlogDetailView, BlogListView


urlpatterns = [
    path("blog/", BlogListView.as_view(), name="blog-list"),
    path("blog/<str:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
