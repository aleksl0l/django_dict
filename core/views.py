from rest_framework import viewsets, generics

from .models import User, Set
from .serializers import UserSerializer, SetSerializer, AddWordsSerializer, SetDetailSerializer


class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()


class SetViewSet(viewsets.ModelViewSet):
    serializer_class = SetSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SetDetailSerializer
        return SetSerializer

    def get_queryset(self):
        queryset = Set.objects.all()
        username = self.request.query_params.get('user', None)
        if username is not None:
            queryset = queryset.filter(user__name=username)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        return super().create(request, *args, **kwargs)


class WordCreateView(generics.CreateAPIView):
    serializer_class = AddWordsSerializer
    queryset = Set.objects.all()
    lookup_url_kwarg = 'set_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(user=self.request.user, set=self.get_object())
        return context
