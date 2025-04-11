from rest_framework import serializers

from blog.models import BlogPost


class BlogListSerializer(serializers.ModelSerializer):
    """
    Serializer for the list of blog posts.
    """

    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["title", "slug", "content", "created_at", "updated_at", "author"]

    def get_author(self, obj):
        return obj.author.username


class BlogDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for a single blog post.
    """

    author = serializers.SerializerMethodField()
    comments = serializers.ListField(
        child=serializers.CharField(max_length=255), required=False, default=[]
    )

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "content",
            "created_at",
            "updated_at",
            "author",
            "comments",
        ]

    def get_author(self, obj):
        return obj.author.username
