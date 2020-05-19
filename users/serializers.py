from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserImage
# from recipes.serializers import RecipeSerializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'

    def to_representation(self, instance):
        image = instance.image
        if image:
            url = instance.image.url
            request = self.context.get('request', None)

            if request is not None:
                return request.build_absolute_uri(url)

            return url
        else:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'image')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    image = ImageSerializer(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            is_active = False
        )
        return user
