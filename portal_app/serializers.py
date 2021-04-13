from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal_app.models import Like, Post, Groupe, Category, AdditionalInfo


class AdditionalInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'motorcycle', 'date_of_birth', 'city']

    motorcycle = serializers.CharField(source='additionalinfo.motorcycle')  # this is your related_name
    date_of_birth = serializers.DateField(source='additionalinfo.date_of_birth')  # this is your related_name
    city = serializers.CharField(source='additionalinfo.city')  # this is your related_name


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class GroupeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Like
        fields = '__all__'
