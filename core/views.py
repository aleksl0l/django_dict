from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Users, Sets, Setsandword, Words
from .serializers import UsersSerializer, SetsSerializer


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class SetsByUserView(generics.ListAPIView):
    serializer_class = SetsSerializer

    def get_queryset(self):
        queryset = Sets.objects.all()
        username = self.request.query_params.get('user', None)
        if username is not None:
            queryset = queryset.filter(user__name=username)
        return queryset


class UsersList(APIView):
    def get(self, request, format=None):
        snippets = Users.objects.all()
        serializer = UsersSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


