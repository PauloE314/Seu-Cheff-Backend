from rest_framework.views import APIView, Response
from config import FOOD_TYPES



class Config(APIView):
    def get(self, request, *args, **kwargs):
        return Response(FOOD_TYPES)