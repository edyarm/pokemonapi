from rest_framework import generics
from .models import Pokemon
from .serializers import PokemonSerializer
from itertools import chain
from django.shortcuts import get_object_or_404


class PokemonList(generics.ListCreateAPIView):
    serializer_class = PokemonSerializer

    def get_queryset(self):
        pokemons = list(Pokemon.objects.all())
        for pokemon in pokemons:
            pre_evolutions = list(Pokemon.objects.filter(evolution_to=pokemon.id))
            evolutions = list(pokemon.evolution_to.all())
            for evolution in evolutions:
                evolution.type = "Evolution"
            if pre_evolutions:
                for pre in pre_evolutions:
                    pre.type = "Preevolution"
                evolutions = list(chain(evolutions, pre_evolutions))
            pokemon.evolutions = evolutions
        return pokemons


class PokemonDetail(generics.RetrieveAPIView):
    lookup_field = "name"
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        filter[self.lookup_field] = self.kwargs[self.lookup_field]
        pokemon = get_object_or_404(queryset, **filter)
        pre_evolutions = list(Pokemon.objects.filter(evolution_to=pokemon.id))
        evolutions = list(pokemon.evolution_to.all())
        for evolution in evolutions:
            evolution.type = "Evolution"
        if pre_evolutions:
            for pre in pre_evolutions:
                pre.type = "Preevolution"
            evolutions = list(chain(evolutions, pre_evolutions))
        pokemon.evolutions = evolutions
        return pokemon
