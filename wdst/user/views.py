# from django.shortcuts import render
from rest_framework import viewsets
from user.models import Users
from user.serializers import UsersSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from user.forms import RegisterForm
from user.generate_token import generate_jwt_token
from utils.jwt_permission_required import auth_permission_required
from utils.common import result


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):

    queryset = Users.objects.all()
    serializer_class = UsersSerializers


class UsersList(APIView):
    # 定义 GET 请求的方法，内部实现相同 @api_view
    """
        get:
            Return all Users.
        post:
            Create a new Users.
    """
    def get(self, request):
        user = Users.objects.all()
        serializer = UsersSerializers(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 定义 POST 请求的方法
    def post(self, request):
        serializer = UsersSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersDetail(APIView):
    """
        get:
            Return a Users instance.
        put:
            Update a Users.
        patch:
            Update one or more fields on an existing Users.
    """
    def get_Users(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_Users(pk)
        serializer = UsersSerializers(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_Users(pk)
        serializer = UsersSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ## to permit delete action or not
    def delete(self, request, pk):
        user = self.get_Users(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    def post(self, request):
        result["message"] = "登录失败"
        result["success"] = False
        result["details"] = None
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            username = python_data.get('username')
            password = python_data.get('password')
            data = Users.objects.filter(username=username, password=password).values("id", "username").first()
            if data:
                token = generate_jwt_token(username)
                result["message"] = "登录成功"
                result["success"] = True
                result["details"] = {"id": data["id"], "username": data["username"],"token": token}
                return JsonResponse(result, status=200)
            result["details"] = "用户名或密码错误"
            return JsonResponse(result, status=400)
        return JsonResponse(result, status=500)


class RegisterView(APIView):
    def post(self, request):
        result["message"] = "注册失败"
        result["success"] = False
        result["details"] = None
        json_data = request.body.decode('utf-8')
        if json_data:
            python_data = eval(json_data)
            data = RegisterForm(python_data)
            if data.is_valid():
                data.cleaned_data.pop("r_password")
                Users.objects.create(**data.cleaned_data)
                data.cleaned_data.pop("password")
                result["message"] = "注册成功"
                result["success"] = True
                result["details"] = data.cleaned_data
                return JsonResponse(result, status=200)
            else:
                result["details"] = data.errors
                return JsonResponse(result, status=400)
        return JsonResponse(result, status=500)

@auth_permission_required("func")
def demo(request):
    if request.method == 'GET':
        return JsonResponse({"state": 1, "message": "token有效"})
    else:
        return JsonResponse({"state": 0, "message": "token无效"})
