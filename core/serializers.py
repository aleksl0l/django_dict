from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.tasks import update_meaning_cam
from .models import User, Set, Word, Meaning


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )


class SetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = ('id', 'name', 'description', 'user')
        extra_kwargs = {'description': {'required': False}}


class MeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meaning
        fields = ('id', 'meaning', 'examples')


class WordsSerializer(serializers.ModelSerializer):
    meanings = MeaningSerializer(many=True)

    class Meta:
        model = Word
        fields = ('id', 'word', 'meanings')


class SetDetailSerializer(serializers.ModelSerializer):
    words = WordsSerializer(many=True)

    class Meta:
        model = Set
        fields = ('id', 'name', 'description', 'user', 'words')


class AddWordsSerializer(serializers.Serializer):
    words = serializers.ListField(child=serializers.CharField(max_length=40))

    def validate(self, attrs):
        user = self.context.get('user')
        set_instance = self.context.get('set')
        if set_instance.user != user:
            raise ValidationError('You don\'t own this set')
        return attrs

    @atomic
    def create(self, validated_data):
        words = validated_data.pop('words')
        set_instance: Set = self.context.get('set')
        words_instances = Word.objects.filter(word__in=words)
        words_set = set(words_instances.values_list('word', flat=True))
        words_instances = list(words_instances)
        with atomic():
            self.create_words(words, words_instances, words_set)
        set_instance.words.add(*words_instances)
        return set_instance

    def create_words(self, words, words_instances, words_set):
        for word in words:
            if word not in words_set:
                word_instance = Word.objects.create(word=word)
                update_meaning_cam.delay(word_instance.id)
                words_instances.append(word_instance)

    def to_representation(self, instance):
        return SetDetailSerializer(instance).data
