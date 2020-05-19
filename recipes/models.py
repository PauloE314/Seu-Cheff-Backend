from django.db import models
from django.contrib.postgres.fields import ArrayField 
from django.contrib.auth.models import User
from extension.models_methods import delete_file, exist
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete

import config

class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")

    time = models.FloatField()
    food_yield = models.IntegerField()

    ingredients = ArrayField(
        models.CharField(max_length=100)
    )

    steps = ArrayField(
        models.TextField()
    )
    additional_information = models.TextField(blank=True)
    food_type = models.CharField(choices=config.FOOD_TYPES, max_length=5, blank=True)

    favorited = models.ManyToManyField(User, related_name='favorites', blank=True)

    @property
    def favorites(self):
        return len(self.favorited.all())


# #IMAGE
@receiver(pre_save, sender=Recipe)
def handle_update_recipe(sender, instance=None, **kwargs):
    if exist(instance=instance, model=sender):
        old_recipe = Recipe.objects.get(pk=instance.pk)

        delete_file(instance=old_recipe, file_name="image")


# @receiver(pre_delete, sender=Recipe)
# def handle_delete_recipe(sender, instance=None, **kwargs):
#     delete_file(instance=instance, file_name="image")