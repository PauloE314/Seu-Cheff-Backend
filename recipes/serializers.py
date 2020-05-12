from rest_framework import serializers
from recipes.models import Recipe
from django.contrib.auth.models import User
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['favorited',]
        read_only_fields = ('image', )
        extra_kwargs = {
            'food_type': {"required":True}
        }

    favorites = serializers.IntegerField(read_only=True)

    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance, *args, **kwargs)
        data['author'] = UserSerializer(instance.author).data
        data['food_type'] = instance.get_food_type_display()

        return data

    