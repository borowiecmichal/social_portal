from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from django.test import Client

# def test_details(client):
#     response = client.get('sith/list/')  # Pobieramy stronę metodą GET.
#     assert response.status_code == 200  # Czy odpowiedź HTTP to 200 OK.
#     # Czy widok zwrócił w kontekście DOKŁADNIE 2 Sithów?
#     assert len(response.context['sith']) == 2
#
from portal_app.models import Post, Groupe


# def test_LandingView(client):
#     response = client.get('')
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_registration(client):
#     response = client.get('/register/')
#     assert response.status_code == 200
#
#     response = client.post('/register/', {
#         'username': 'aagngcv.jjj',
#         'first_name': 'John',
#         'last_name': 'Smith',
#         'password': 'Portalik123',
#         'password2': 'Portalik123',
#         'email': 'jsd@dkk.com',
#         'motorcycle': 'CBF500',
#         'date_of_birth': '2000-01-01',
#         'city': 'London'
#     })
#
#     assert response.status_code == 302
#     assert User.objects.get(username='aagngcv.jjj')
#
#
# @pytest.mark.django_db
# def test_login(client, exmp_user):
#     assert User.objects.all().count() == 1
#     resp = client.post('/login/', {
#         'username': 'aagngcv.jjj',
#         'password': 'Portalik123'
#     })
#     assert resp.status_code == 302
#
#     resp = client.post('/login/', {
#         'username': 'aagngcv.jjjj',
#         'password': 'Portalik123'
#     })
#     assert resp.status_code == 200
#     assert resp.context['error'] == 'Błędne dane logowania'
#
#
# @pytest.mark.django_db
# def test_profile_view(client, exmp_user, posts_3):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     assert exmp_user.username == 'aagngcv.jjj'
#     resp = client.get(f'/profile/{exmp_user.username}')
#     assert resp.context['user_requested'] == exmp_user
#     assert resp.context['content_post'][2] == posts_3[0]
#     assert resp.context['content_post'][0] == posts_3[2]
#     assert resp.context['content_post'][1] == posts_3[1]
#     assert resp.status_code == 200
#
#
# @pytest.mark.django_db
# def test_post_create_view(client, exmp_user):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.post('/add_post/', {'content': 'abcdefg'})
#     assert resp.status_code == 302
#     resp = client.get(f'/profile/{exmp_user.username}')
#     assert resp.context['user_requested'] == exmp_user
#     assert resp.context['content_post'][0].content == 'abcdefg'
#
#
# @pytest.mark.django_db
# def test_profile_edit_view(client, exmp_user):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.get(f'/profile/{exmp_user.username}/edit')
#     assert resp.status_code == 200
#     resp = client.post(f'/profile/{exmp_user.username}/edit', {
#         'username': exmp_user.username,
#         'first_name': 'Antonio',
#         'last_name': exmp_user.last_name,
#         'email': exmp_user.email,
#         'motorcycle': exmp_user.additionalinfo.motorcycle,
#         'date_of_birth': exmp_user.additionalinfo.date_of_birth,
#         'city': exmp_user.additionalinfo.city
#     })
#     assert resp.status_code == 302
#     assert User.objects.get(username=exmp_user.username).first_name == 'Antonio'
#
#
# @pytest.mark.django_db
# def test_comment_post_view(client, exmp_user, posts_3):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     assert exmp_user.username == 'aagngcv.jjj'
#     resp = client.get(f'/comment-post/{posts_3[0].id}')
#     assert resp.status_code == 200
#
#     resp = client.post(f'/comment-post/{posts_3[0].id}', {'content': 'test_comm'})
#     assert Post.objects.get(pk=posts_3[0].id).comment_set.all().count() == 1
#     assert resp.status_code == 302
#
#
# @pytest.mark.django_db
# def test_list_group_view(client, groupe):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.get(f'/groups/')
#     assert resp.status_code == 200
#     assert resp.context['object_list'][0] == Groupe.objects.all()[0]
#     assert resp.context['object_list'].count() == Groupe.objects.all().count()
#
#
# @pytest.mark.django_db
# def test_append_group_view(client, exmp_user, groupe):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.get(f'/group/{groupe.slug}/append')
#     assert resp.status_code == 302
#     assert User.objects.get(pk=exmp_user.id).groupe_set.all().count() == 1
#
#
# @pytest.mark.django_db
# def test_group_details_view(client, exmp_user, groupe):
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.get(f'/group/{groupe.slug}/')
#     assert resp.status_code == 200
#     assert resp.context['object'].name == groupe.name
#
#
# @pytest.mark.django_db
# def test_group_create_view(client, exmp_user, category):
#     client.logout()
#     resp = client.get(f'/create-group/')
#     assert resp.status_code == 302
#
#     client.login(username='aagngcv.jjj', password='Portalik123')
#     resp = client.get(f'/create-group/')
#     assert resp.status_code == 200
#
#     assert Groupe.objects.all().count() == 0
#     resp = client.post(f'/create-group/', {
#         'name': 'przykladowa Grupa',
#         'category': category
#     })
#     assert resp.status_code == 200
# #tutaj nie działa zliczanie!!!

@pytest.mark.django_db
def test_users_group_view(client, exmp_user, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/{exmp_user.username}/groups/')
    assert resp.status_code == 200
    assert len(resp.context['object_list']) == 1


@pytest.mark.django_db
def test_messages_view(client, exmp_user, exmp_user2):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/messages/')
    assert resp.status_code == 200
    # assert len(resp.context['object_list']) == 2
