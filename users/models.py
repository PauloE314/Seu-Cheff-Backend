from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail, EmailMessage
from django.utils.crypto import get_random_string
from extension.models_methods import exist, delete_file

from receitas_backend.settings import EMAIL_HOST_USER

class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="activation_token")
    key = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.key


class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to="users", blank=True)


# CREATE IMAGE OBJECT
@receiver(post_save, sender=User)
def create_user_image(sender, instance=None, created=None, **kwargs):
    if created:
        user_image = UserImage.objects.create(user=instance)


# UPDATE IMAGE HANDLER
@receiver(pre_save, sender=UserImage)
def handle_update_recipe(sender, instance=None, **kwargs):
    if exist(instance=instance, model=sender):
        old_user_image = UserImage.objects.get(pk=instance.pk)

        delete_file(instance=old_user_image, file_name="image")



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        login_token = Token.objects.create(user=instance)
        activation_token = ActivationToken.objects.create(user=instance)

@receiver(pre_save, sender=ActivationToken)
def create_validation_token(sender, instance=None, **kwargs):
    queryset = ActivationToken.objects.all()

    if instance not in queryset:
        instance.key = get_random_string(length=8)

@receiver(post_save, sender=ActivationToken)
def send_validation_email(sender, instance, **kwargs):
    subject = 'Ativação de conta - Receitas'
    message = f"Ativação de email, Token de ativação: {instance}"

    sending_email = EmailMessage(subject, message, EMAIL_HOST_USER, [instance.user.email])

    sending_email.content_subtype = "html"

    sending_email.send()