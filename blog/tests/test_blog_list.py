import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from blog.models import BlogPost 

User = get_user_model()

class TestBlogListView:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """
        테스트 데이터를 설정합니다.
        """
        # 테스트용 사용자 생성
        self.user1 = User.objects.create_user(
            username="author1",
            email="author1@example.com",
            password="password123"
        )
        
        self.user2 = User.objects.create_user(
            username="author2",
            email="author2@example.com",
            password="password123"
        )
        
        # 테스트용 블로그 게시물 생성
        self.post1 = BlogPost.objects.create(
            title="First Post",
            slug="first-post",
            content="This is the first post.",
            author=self.user1
        )
        
        self.post2 = BlogPost.objects.create(
            title="Second Post",
            slug="second-post",
            content="This is the second post.",
            author=self.user2
        )
        
        self.url = reverse("blog-list")
        self.client = APIClient()

    def test_blog_list_view(self):
        """
        블로그 목록 API 뷰를 테스트합니다.
        """
        response = self.client.get(self.url)
        assert response.status_code == 200
        
        # 응답 데이터가 리스트인지 확인
        assert isinstance(response.data, list)
        
        # 생성한 두 게시물이 응답에 포함되어 있는지 확인
        assert len(response.data) >= 2
        
        # 응답 데이터에서 게시물 찾기
        first_post = next((post for post in response.data if post["slug"] == "first-post"), None)
        assert first_post is not None
        assert first_post["title"] == "First Post"
        assert first_post["content"] == "This is the first post."
        assert "created_at" in first_post
        assert "updated_at" in first_post

        assert first_post["author"] == "author1"
        
        # 두 번째 게시물 검증
        second_post = next((post for post in response.data if post["slug"] == "second-post"), None)
        assert second_post is not None
        assert second_post["title"] == "Second Post"
