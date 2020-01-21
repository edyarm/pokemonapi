from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('pokemons/', views.PokemonList.as_view()),
    path('pokemons/<str:name>/', views.PokemonDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
