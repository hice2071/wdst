from user.models import Users
from rest_framework import serializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


# class UsersList(APIView):
#     # 定义 GET 请求的方法，内部实现相同 @api_view
#     def get(self, request):
#         Users = Users.objects.all()
#         serializer = UsersSerializer(Users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     # 定义 POST 请求的方法
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         User = self.get_object(pk)
#         serializer = UserSerializer(User)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         User = self.get_object(pk)
#         serializer = UserSerializer(User, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     ## to permit delete action or not
#     # def delete(self, request, pk):
#     #     User = self.get_object(pk)
#     #     User.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
