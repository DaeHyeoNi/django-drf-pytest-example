from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost
from blog.serializers import BlogDetailSerializer, BlogListSerializer


class BlogListView(APIView):
    """
    A simple API view that returns a list of blog posts.
    """

    def get(self, request):
        """
        Returns a list of blog posts.
        """
        blog_posts = BlogPost.objects.all()
        serializer = BlogListSerializer(blog_posts, many=True)
        return Response(serializer.data)


class BlogDetailView(APIView):
    """
    A simple API view that returns a single blog post.
    """

    def get(self, request, slug):
        """
        Returns a single blog post.
        """
        blog_post = get_object_or_404(BlogPost, slug=slug)
        serializer = BlogDetailSerializer(blog_post)
        return Response(serializer.data)
