from rest_framework import serializers
from recipes.models import Recipe
from django.contrib.auth.models import User
from users.serializers import UserSerializer, ImageSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['favorited',]
        read_only_fields = ('image', 'created_at', 'last_update')
        extra_kwargs = {
            'food_type': {"required":True}
        }

    favorites = serializers.IntegerField(read_only=True)

    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance, *args, **kwargs)
        data['author'] = UserSerializer(instance.author).data
        data['food_type'] = instance.get_food_type_display()

        return data



class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'recipes', 'image')
        
    image = ImageSerializer(read_only=True)
    recipes = RecipeSerializer(many=True)
    



    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance, *args, **kwargs)
        
        for item in data['recipes']:
            item.pop('author')

        return data