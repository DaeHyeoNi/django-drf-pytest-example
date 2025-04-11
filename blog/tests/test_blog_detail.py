import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from blog.models import BlogPost

User = get_user_model()


class TestBlogDetailView:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """
        테스트 데이터를 설정합니다.
        """
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(
            username="testauthor",
            email="testauthor@example.com",
            password="password123"
        )
        
        # 테스트용 블로그 게시물 생성
        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post content.",
            author=self.user
        )
        
        self.client = APIClient()
        
    def test_blog_detail_view_success(self):
        """
        존재하는 slug로 블로그 상세 보기를 요청할 경우 성공하는지 테스트합니다.
        """
        url = reverse("blog-detail", kwargs={"slug": "test-post"})
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert response.data["title"] == "Test Post"
        assert response.data["slug"] == "test-post"
        assert response.data["content"] == "This is a test post content."
        assert "created_at" in response.data
        assert "updated_at" in response.data
        
        # Serializer가 author 필드를 어떻게 처리하는지에 따라 조정
        # 예: 사용자 이름만 반환하는 경우
        assert response.data["author"] == "testauthor"
        
    def test_blog_detail_view_not_found(self):
        """
        존재하지 않는 slug로 블로그 상세 보기를 요청할 경우 404를 반환하는지 테스트합니다.
        """
        url = reverse("blog-detail", kwargs={"slug": "non-existent-post"})
        response = self.client.get(url)
        
        assert response.status_code == 404
        
    @pytest.mark.parametrize(
        "field,expected_value", 
        [
            ("title", "Test Post"),
            ("content", "This is a test post content."),
            ("slug", "test-post"),
        ]
    )
    def test_blog_detail_fields(self, field, expected_value):
        """
        블로그 상세 응답의 각 필드가 예상대로 반환되는지 테스트합니다.
        """
        url = reverse("blog-detail", kwargs={"slug": "test-post"})
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert response.data[field] == expected_value
