from django.core.exceptions import FieldDoesNotExist
import json
from collections import Iterable
from django.db.models.fields import related

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