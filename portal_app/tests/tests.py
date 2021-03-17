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


def test_LandingView(client):
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration(client):
    response = client.get('/register/')
    assert response.status_code == 200

    response = client.post('/register/', {
        'username': 'johnny',
        'first_name': 'John',
        'last_name': 'Smith',
        'password1': 'Portalik123',
        'password2': 'Portalik123',
        'email': 'jsd@dkk.com',
        'motorcycle': 'CBF500',
        'date_of_birth_day': '1',
        'date_of_birth_month': '1',
        'date_of_birth_year': '1980',
        'city': 'London'
    })

    assert response.status_code == 302


@pytest.mark.django_db
def test_login(client, exmp_user):
    assert User.objects.all().count() == 1
    resp = client.post('/login/', {
        'username': 'aagngcv.jjj',
        'password': 'Portalik123'
    })
    assert resp.status_code == 302

    resp = client.post('/login/', {
        'username': 'aagngcv.jjjj',
        'password': 'Portalik123'
    })
    assert resp.status_code == 200
    assert resp.context['error'] == 'Błędne dane logowania'


@pytest.mark.django_db
def test_logout(client, exmp_user):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/logout/')
    # assert client.request.get('user')
    assert resp.status_code == 302


@pytest.mark.django_db
def test_profile_view(client, exmp_user, posts_3):
    client.login(username='aagngcv.jjj', password='Portalik123')
    assert exmp_user.username == 'aagngcv.jjj'
    resp = client.get(f'/profile/{exmp_user.username}')
    assert resp.context['user_requested'] == exmp_user
    assert resp.context['content_post'][2] == posts_3[0]
    assert resp.context['content_post'][0] == posts_3[2]
    assert resp.context['content_post'][1] == posts_3[1]
    assert resp.status_code == 200


@pytest.mark.django_db
def test_post_create_view(client, exmp_user):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.post('/add_post/', {'content': 'abcdefg'})
    assert resp.status_code == 302
    resp = client.get(f'/profile/{exmp_user.username}')
    assert resp.context['user_requested'] == exmp_user
    assert resp.context['content_post'][0].content == 'abcdefg'


@pytest.mark.django_db
def test_post_like(client, posts_3):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.post(f'/like-post/{posts_3[0].id}/')
    post_liked = Post.objects.get(pk=posts_3[0].id)
    assert post_liked.likes == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_profile_edit_view(client, exmp_user):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/profile/{exmp_user.username}/edit')
    assert resp.status_code == 200
    resp = client.post(f'/profile/{exmp_user.username}/edit', {
        'username': exmp_user.username,
        'first_name': 'Antonio',
        'last_name': exmp_user.last_name,
        'email': exmp_user.email,
        'motorcycle': exmp_user.additionalinfo.motorcycle,
        'date_of_birth': exmp_user.additionalinfo.date_of_birth,
        'city': exmp_user.additionalinfo.city
    })
    assert resp.status_code == 302
    assert User.objects.get(username=exmp_user.username).first_name == 'Antonio'


@pytest.mark.django_db
def test_comment_post_view(client, exmp_user, posts_3):
    client.login(username='aagngcv.jjj', password='Portalik123')
    assert exmp_user.username == 'aagngcv.jjj'
    resp = client.get(f'/comment-post/{posts_3[0].id}')
    assert resp.status_code == 200

    resp = client.post(f'/comment-post/{posts_3[0].id}', {'content': 'test_comm'})
    assert Post.objects.get(pk=posts_3[0].id).comment_set.all().count() == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_list_group_view(client, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/groups/')
    assert resp.status_code == 200
    assert resp.context['object_list'][0] == Groupe.objects.all()[0]
    assert resp.context['object_list'].count() == Groupe.objects.all().count()


@pytest.mark.django_db
def test_add_post_to_group_view(client, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')

    resp = client.get(f'/group/{groupe.slug}/add_post/')
    assert resp.status_code == 200

    resp = client.post(f'/group/{groupe.slug}/add_post/', {'content': 'test_post'})
    group = Groupe.objects.get(pk=groupe.id)
    assert resp.status_code == 302
    assert group.post_set.all().count() == 1


@pytest.mark.django_db
def test_append_group_view(client, exmp_user, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/group/{groupe.slug}/append')
    assert resp.status_code == 302
    assert User.objects.get(pk=exmp_user.id).groupe_set.all().count() == 1


@pytest.mark.django_db
def test_group_details_view(client, exmp_user, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/group/{groupe.slug}/')
    assert resp.status_code == 200
    assert resp.context['object'].name == groupe.name


@pytest.mark.django_db
def test_group_create_view(client, exmp_user, category):
    client.logout()
    resp = client.get(f'/create-group/')
    assert resp.status_code == 302

    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/create-group/')
    assert resp.status_code == 200

    assert Groupe.objects.all().count() == 0
    resp = client.post(f'/create-group/', {
        'name': 'przykladowa Grupa',
        'category': category
    })
    assert resp.status_code == 200


# tutaj nie działa zliczanie!!!

@pytest.mark.django_db
def test_users_group_view(client, exmp_user, groupe):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/{exmp_user.username}/groups/')
    assert resp.status_code == 200
    assert len(resp.context['object_list']) == 1


@pytest.mark.django_db
def test_delete_group_view(client, exmp_user, groupe, groupe_with_mod):
    assert Groupe.objects.all().count() == 2
    client.login(username='aagngcv.jjj', password='Portalik123')

    resp = client.get(f'/groups/delete/{groupe.slug}/')
    assert resp.status_code == 403

    resp = client.post(f'/groups/delete/{groupe.slug}/')
    assert resp.status_code == 403

    resp = client.get(f'/groups/delete/{groupe_with_mod.slug}/')
    assert resp.status_code == 200

    resp = client.post(f'/groups/delete/{groupe_with_mod.slug}/')
    assert resp.status_code == 302

    assert Groupe.objects.all().count() == 1


@pytest.mark.django_db
def test_group_requests_view(client, exmp_user, groupe, groupe_with_mod):
    client.login(username='aagngcv.jjj', password='Portalik123')

    resp = client.get(f'/groups/requests-users/{groupe.slug}/')
    assert resp.status_code == 403

    resp = client.get(f'/groups/requests-users/{groupe_with_mod.slug}/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_group_request_accept_view(client, exmp_user, exmp_user2, groupe, groupe_with_mod):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/groups/requests-users/{groupe.slug}/accept/{exmp_user2.username}/')
    assert resp.status_code == 403

    resp = client.get(f'/groups/requests-users/{groupe_with_mod.slug}/accept/{exmp_user2.username}/')
    assert resp.status_code == 302
    g = Groupe.objects.get(pk=groupe_with_mod.id)
    assert g.to_join.all().count() == 0
    assert g.users.all().count() == 2


@pytest.mark.django_db
def test_group_request_reject_view(client, exmp_user, exmp_user2, groupe, groupe_with_mod):
    client.login(username='aagngcv.jjj', password='Portalik123')

    resp = client.get(f'/groups/requests-users/{groupe.slug}/reject/{exmp_user2.username}/')
    assert resp.status_code == 403

    resp = client.get(f'/groups/requests-users/{groupe_with_mod.slug}/reject/{exmp_user2.username}/')
    assert resp.status_code == 302
    g = Groupe.objects.get(pk=groupe_with_mod.id)
    assert g.to_join.all().count() == 0
    assert g.users.all().count() == 1


@pytest.mark.django_db
def test_group_leave_view(client, exmp_user, exmp_user2, groupe, groupe_with_mod_and_2users):
    client.login(username='aagngcv.jjj2', password='Portalik123')

    resp = client.get(f'/groups/leave/{groupe.slug}/')
    assert resp.status_code == 403

    resp = client.get(f'/groups/leave/{groupe_with_mod_and_2users.slug}/')
    assert resp.status_code == 302
    g = Groupe.objects.get(pk=groupe_with_mod_and_2users.id)
    assert g.to_join.all().count() == 0
    assert g.users.all().count() == 1


@pytest.mark.django_db
def test_messageswituser_view(client, exmp_user, exmp_user2):
    client.login(username='aagngcv.jjj', password='Portalik123')
    resp = client.get(f'/messages/{exmp_user2.username}')
    assert resp.status_code == 200

    resp = client.post(f'/messages/{exmp_user2.username}', {'message': 'wiadomosc1'})
    assert resp.status_code == 302

    resp = client.get(f'/messages/{exmp_user2.username}')
    assert resp.status_code == 200
    assert len(resp.context['messages']) == 1


@pytest.mark.django_db
def test_messages_view(client, exmp_user, exmp_user2):
    resp = client.get('/messages/')
    assert resp.status_code == 302
