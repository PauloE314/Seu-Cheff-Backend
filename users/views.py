from django.contrib.auth.models import User
from rest_framework.views import APIView, Response
from rest_framework import status
from users.models import ActivationToken
from users.serializers import UserSerializer
from extension import class_views


class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("Hello World")

class Users(class_views.SearchListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    
    searching_fields = ["username"]
    searching_models = [("", User)]
    order_by = ["username"]



class ActiveAccount(APIView):
    def post(self, request, *args, **kwargs):
        activation_token = request.data.get('activation_token')

        if activation_token:
            try:
                user = ActivationToken.objects.get(key=activation_token).user
                user.is_active = True
                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data)

            except ActivationToken.DoesNotExist:
                return Response({'Senha de ativação inválida'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Envie uma senha de autenticação'}, status=status.HTTP_400_BAD_REQUEST)