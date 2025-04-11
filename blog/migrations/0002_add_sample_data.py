from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_sample_data(apps, schema_editor):
    # 모델을 가져옵니다
    BlogPost = apps.get_model('blog', 'BlogPost')
    User = apps.get_model('auth', 'User')
    
    # 사용자가 이미 있는지 확인하고 없으면 생성합니다
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True,
            password=make_password('admin123')  # set_password 대신 make_password 사용
        )
    else:
        admin_user = User.objects.get(username='admin')
    
    # 블로그 게시물을 생성합니다
    BlogPost.objects.create(
        title='샘플 블로그 게시물',
        slug='sample-blog-post',
        content='이것은 마이그레이션을 통해 생성된 샘플 블로그 게시물입니다. Django 마이그레이션은 데이터를 생성하는 데도 사용될 수 있습니다.',
        author=admin_user
    )


def remove_sample_data(apps, schema_editor):
    # 되돌릴 때 실행되는 함수입니다
    BlogPost = apps.get_model('blog', 'BlogPost')
    BlogPost.objects.filter(slug='sample-blog-post').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, remove_sample_data),
    ]
