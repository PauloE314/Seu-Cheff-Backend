from rest_framework.permissions import BasePermission
from django.contrib.auth import authenticate


def check_auth(request):
    auth_data = request.data.get('authorization')
    
    if auth_data:
        username = auth_data.get('username')
        password = auth_data.get('password')

        auth = authenticate(username=username, password=password)
        print(auth)

        return auth and auth == request.user
    else:
        return False
    


class GetOnly(BasePermission):
    def has_permission(self, request, *args, **kwargs):
        return request.method == "GET"


class CheckAuth(BasePermission):
    message = "Forneça suas credenciais (senha e nome de usuário)"

    def has_permission(self, request, *args, **kwargs):
        return check_auth(request)


class CheckAuthOnDelete(BasePermission):
    def has_permission(self, request, *args, **kwargs):
        return check_auth(request) or request.method != 'DELETE'