from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"Name: {self.username} | ID: {self.id}"


class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Meaning(models.Model):
    meaning = models.TextField()
    word = models.ForeignKey(to='Word', related_name='meanings', on_delete=models.SET_NULL, null=True)
    examples = ArrayField(models.TextField())

    def __str__(self):
        return self.meaning


class Word(models.Model):
    NOUN = 'noun'
    ADJECTIVE = 'adjective'
    VERB = 'verb'
    ADVERB = 'adverb'
    PRONOUN = 'pronoun'
    PREPOSITION = 'preposition'
    CONJUNCTION = 'conjunction'
    INTERJECTION = 'interjection'
    PART_OF_SPEECH = (
        (NOUN, 'Noun'),
        (ADJECTIVE, 'Adjective'),
        (VERB, 'Verb'),
        (ADVERB, 'Adverb'),
        (PRONOUN, 'Pronoun'),
        (PREPOSITION, 'Preposition'),
        (CONJUNCTION, 'Conjunction'),
        (INTERJECTION, 'Interjection'),
    )
    word = models.CharField(max_length=40, unique=True)
    sets = models.ManyToManyField(to=Set, related_name='words')
    part_of_speech = models.TextField(choices=PART_OF_SPEECH, null=True)

    def __str__(self):
        return self.word
