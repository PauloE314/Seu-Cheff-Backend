from extension.models_methods import check_field, check_related
from rest_framework import generics, status, mixins
from django.core.exceptions import FieldError
from collections import Iterable

class SearchListAPIView(generics.ListAPIView):
    searching_fields = []
    searching_models = []
    order_by = []

    def final_ordination(self, filtered_queryset, *args, **kwargs):
        return filtered_queryset        

    def get_queryset(self, *args, **kwargs):
        return self.search_and_ordinate(
            self.queryset.all(),
            self.request.query_params,
            *args, **kwargs
        )

    def search_and_ordinate(self, initial_queryset, query_params, *args, **kwargs):
        queryset = initial_queryset
        order_by = list()

        for related_name, model in self.searching_models:
            queryset = self.search(
                fields=self.searching_fields,
                model=model,
                query_params=query_params,
                initial_queryset=queryset,
                relational_name=related_name
            )
        
        for order in self.order_by:
            name = order
            if order[0] == '-':
                name = order[1:]
            
            if check_field(model, name):
                order_by.append(order)
        
        queryset = queryset.order_by(*order_by)
        
        return self.final_ordination(queryset, self.request, initial_queryset, query_params, *args, **kwargs)


    def search(self, fields=None, model=None, query_params=None, initial_queryset=None, relational_name=None):
        request_filters = query_params
        filters = {}
        if not initial_queryset:
            initial_queryset = model.objects.all()
        

        for field in query_params:
            if check_field(model, field) and field in fields:
                value = query_params[field]
                filter_name = f"{field}"

                if relational_name:
                    filter_name = f"{relational_name}__{filter_name}"

                if check_related(model, field):
                    filter_name = f"{filter_name}__pk"
            
                filters[filter_name] = value

        queryset = initial_queryset.filter(**filters)
            
        return queryset


class SearchListCreateAPIView(generics.CreateAPIView, SearchListAPIView):
    pass


class SelfAPIView(generics.GenericAPIView):
    user_relation = None

    def get_object(self, *args, **kwargs):
        if not self.user_relation:
            return self.request.user
        else:
            return super().get_object(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.user_relation:
            user_queryset = getattr(self.request.user, self.user_relation).all()
            return user_queryset
        else:
            return super().get_queryset(self, *args, **kwargs)
        

class SelfRetrieveAPIView(SelfAPIView, generics.RetrieveAPIView):
    pass
    

class SelfUpdateAPIView(SelfAPIView, generics.UpdateAPIView):
    always_partial = None

    def put(self, *args, **kwargs):
        if self.always_partial:
            return super().partial_update(*args, **kwargs)
        return super().put(*args, **kwargs)

class SelfDestroyAPIView(SelfAPIView, generics.DestroyAPIView):
    pass





class SelfRetrieveUpdateAPIView(SelfRetrieveAPIView, SelfUpdateAPIView):
    pass

class SelfRetrieveDestroyAPIView(SelfRetrieveAPIView, SelfDestroyAPIView):
    pass

class SelfRetrieveUpdateDestroyAPIView(SelfRetrieveAPIView, SelfUpdateAPIView, SelfDestroyAPIView):
    pass
