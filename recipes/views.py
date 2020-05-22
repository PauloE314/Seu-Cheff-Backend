from rest_framework.views import Response, APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from extension import class_views
from extension.permissions import CheckAuthOnDelete
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.contrib.auth.models import User


#TODAS AS RECEITAS
class Receipes(class_views.SearchListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    searching_fields = ["title", "food_type", "author"]
    searching_models = [("", Recipe)]

    def get_queryset(self, *args, **kwargs):
        query_params = self.request.query_params
        queryset = super().get_queryset(*args, **kwargs)
        
        # Caso a ordem seja igual a ranking, ordena em função dos favoritos
        if query_params.get('order') == 'ranking':
            queryset = sorted(
                queryset,
                key=lambda recipe: recipe.favorites,
                reverse=True
            )
        # Retorna o queryset
        return queryset


#RECEITA EM ESPECÍFICO
class DetailReceipes(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


#SUAS RECEITAS
class SelfRecipes(class_views.SearchListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    user_relation = 'recipes'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    searching_fields = ["title", "food_type"]
    searching_models = [("", Recipe)]

    def create(self, request, *args, **kwargs):
        data = request.data
        author = request.user.pk

        recipe_serializer = RecipeSerializer(
            data={'author': author, **request.data}
            )

        if recipe_serializer.is_valid():
            recipe_serializer.save()
            return Response(recipe_serializer.data)
        else:
            return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#SUA RECEITA ESPECÍFICA
class DetailSelfRecipes(class_views.SelfRetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & CheckAuthOnDelete]

    user_relation = 'recipes'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    always_partial = True

    def partial_update(self, request, *args, **kwargs):
        if request.data.get('author') or request.data.get('favorited'):
            return Response({'message': "Não é possível alterar o autor ou a quantidade de likes diretamente"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().partial_update(request, *args, **kwargs)


#MUDAR A IMAGEM DA SUA RECEITA
class SetRecipeImage(class_views.SelfRetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    user_relation = 'recipes'
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    always_partial = True
    
    def partial_update(self, request, *args, **kwargs):
        image = request.FILES.get('image')

        if image:
            recipe = self.get_object()
            recipe.image = image
            recipe.save()
            return Response(RecipeSerializer(recipe).data)

        else:
            return Response({'message': 'Envie uma imagem'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        recipe.image = None
        recipe.save()
        return Response(RecipeSerializer(recipe).data)



class FavoriteRecipe(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_object()

        if user in recipe.favorited.all():
            recipe.favorited.remove(user)
            return Response({'message': 'Removido com sucesso'})
        else:
            recipe.favorited.add(user)
            return Response({'message': 'Adicionado com sucesso'})