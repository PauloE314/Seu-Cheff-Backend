from extension.models_methods import check_field, check_related
from rest_framework import generics, status, mixins
from django.core.exceptions import FieldError
from collections import Iterable
from rest_framework.permissions import IsAuthenticated

class SearchListAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    user_relation = None

    searching_fields = []
    searching_models = []
    order_by = ['-pk']

    def get_queryset(self, *args, **kwargs):
        if self.user_relation:
            queryset = getattr(self.request.user, self.user_relation).all()
            
        else:
            queryset = self.queryset.all()

        
        searched_queryset = self.search(
            *args,
            initial_queryset=queryset,
            query_params=self.request.query_params,
            **kwargs
        )

        ordinated_queryset = self.ordinate(searched_queryset, *args, **kwargs)

        return ordinated_queryset



    def search(self, *args, initial_queryset=None, query_params=None, **kwargs):
        queryset = initial_queryset
        for related_name, model in self.searching_models:
            queryset = self.search_field(
                fields=self.searching_fields,
                model=model,
                query_params=query_params,
                initial_queryset=queryset,
                relational_name=related_name
            )
    
        
        return queryset

    def ordinate(self, queryset, *args, **kwargs):
        return queryset.order_by(*self.order_by)


    def search_field(self, fields=None, model=None, query_params=None, initial_queryset=None, relational_name=None):
        request_filters = query_params
        filters = {}
        if initial_queryset == None:
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
    permission_classes = [IsAuthenticated]
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
            return self.partial_update(*args, **kwargs)
        return super().put(*args, **kwargs)

class SelfDestroyAPIView(SelfAPIView, generics.DestroyAPIView):
    pass





class SelfRetrieveUpdateAPIView(SelfRetrieveAPIView, SelfUpdateAPIView):
    pass

class SelfRetrieveDestroyAPIView(SelfRetrieveAPIView, SelfDestroyAPIView):
    pass

class SelfRetrieveUpdateDestroyAPIView(SelfRetrieveAPIView, SelfUpdateAPIView, SelfDestroyAPIView):
    pass
