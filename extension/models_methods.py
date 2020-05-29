from django.core.exceptions import FieldDoesNotExist
import json
from collections import Iterable
from django.db.models.fields import related
import os


RELATED_CLASSES = [related.ForeignKey, related.OneToOneField, related.ManyToManyField]

def update_instance(instance, data):
    for field in data:
        if field in instance.__dict__:
            setattr(instance, field, data[field])
    return instance

def check_field(model, field_name):
    try:
        field = model._meta.get_field(field_name)
        return field
    except FieldDoesNotExist:
        return False


def check_related(model, field_name):
    db_field = check_field(model, field_name)

    if db_field:
        for field_class in RELATED_CLASSES:
            if isinstance(db_field, field_class):
                return True


#IMAGE


# @receiver(pre_delete, sender=Profile)
def delete_file(instance=None, file_name=None, **kwargs):
    file = getattr(instance, file_name) if file_name else instance.image
    print("DELETANDO ARQUIVO...")

    if file:
        print("ARQUIVO EXISTE...")
        try:
            os.remove(file.path)
            print("ARQUIVO ENCONTRADO!")
        except FileNotFoundError:
            print("ARQUIVO NÃO ENCONTRADO!")
            return False


def exist(instance=None, model=None):
    try:
        model.objects.get(pk=instance.pk)
        return True
    except model.DoesNotExist:
        return False