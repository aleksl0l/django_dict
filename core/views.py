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

# class UsersList(APIView):
#     def get(self, request, format=None):
#         users = Users.objects.all()
#         serializer = UsersSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UsersSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

