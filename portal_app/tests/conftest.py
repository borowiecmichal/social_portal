# Tutaj fixtury

# from app.models import Padawan
# import pytest
# @pytest.fixture
# def padawan():
#     padawan = Padawan.objects.create(name="Luke")
#     return padawan

import pytest
from django.contrib.auth.models import User
from django.core.files.images import ImageFile

from portal_app.models import AdditionalInfo, Post, Photo, Groupe, Category


@pytest.fixture
def exmp_user():
    exmp_user = User.objects.create_user(username='aagngcv.jjj',
                                         password='Portalik123',
                                         first_name='John',
                                         last_name='Smith',
                                         email='jsd@dkk.com')
    AdditionalInfo.objects.create(
        user=exmp_user,
        motorcycle='CBF500',
        date_of_birth='2000-01-01',
        city='London'
    )
    return exmp_user

@pytest.fixture
def exmp_user2():
    exmp_user = User.objects.create_user(username='aagngcv.jjj2',
                                         password='Portalik123',
                                         first_name='John',
                                         last_name='Smith',
                                         email='jsd@dk.com')
    AdditionalInfo.objects.create(
        user=exmp_user,
        motorcycle='CBF500',
        date_of_birth='2000-01-01',
        city='London'
    )
    return exmp_user

@pytest.fixture
def posts_3(exmp_user):
    qs = []
    for e in range(3):
        qs.append(Post.objects.create(
            content=f'post testowy {e}',
            user=exmp_user,
        ))
    return qs


# @pytest.fixture
# def photo(exmp_user):
#     photo = Photo.objects.create(user=exmp_user)
#     photo.photo = ImageFile(open('/home/michal/workspace/social_portal/photos/zdjecieMBorowiec_2.jpeg'), 'rb')
#     photo.save()
#     return photo

@pytest.fixture()
def category(exmp_user):
    cat = Category.objects.create(name='przykladowa kategoria')
    return cat


@pytest.fixture()
def groupe(exmp_user, category):
    groupe = Groupe.objects.create(name='przykladowa grupa', category=category)
    groupe.users.add(exmp_user)
    groupe.save()
    return groupe

