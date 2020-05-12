from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.Receipes.as_view()),
    path('<int:pk>', views.DetailReceipes.as_view()),

    path('self/', views.SelfRecipes.as_view()),
    path('self/<int:pk>', views.DetailSelfRecipes.as_view()),
    path('self/<int:pk>/image/', views.SetRecipeImage.as_view()),

    path('self/favorites/', views.SelfFavorites.as_view()),
    path('self/favorite/<int:pk>', views.FavoriteRecipe.as_view())
]
