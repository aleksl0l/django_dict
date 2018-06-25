from rest_framework import serializers
from .models import Users, Sets, Words


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name')


class SetsSerializer(serializers.ModelSerializer):
    # user_name = serializers.ReadOnlyField()

    class Meta:
        model = Sets
        fields = ('id', 'name', 'description', 'user_name')


class WordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Words
        fields = ('id', 'word', 'meaning')
