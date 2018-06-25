from rest_framework.generics import ListAPIView
from .models import Users, Sets, Words
from .serializers import UsersSerializer, SetsSerializer, WordsSerializer


class UsersListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class SetsByUserView(ListAPIView):
    serializer_class = SetsSerializer

    def get_queryset(self):
        queryset = Sets.objects.all()
        username = self.request.query_params.get('user', None)
        if username is not None:
            queryset = queryset.filter(user__name=username)
        return queryset


class WordsListView(ListAPIView):
    serializer_class = WordsSerializer

    def get_queryset(self):
        queryset = Words.objects.filter(sets__id=self.kwargs['pk'])
        return queryset
