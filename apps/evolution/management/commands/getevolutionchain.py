from django.core.management.base import BaseCommand, CommandError
from apps.evolution.models import Pokemon, Stat
import urllib.request
import json


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    url_evolution_chain = 'https://pokeapi.co/api/v2/evolution-chain/{id}/'
    url_pokemon = 'https://pokeapi.co/api/v2/pokemon/{name}/'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs=1, type=int)

    def handle(self, *args, **options):
        next_chain = True
        self.get_evolution_chain(next(iter(options["id"]), None))
        self.stdout.write(self.style.SUCCESS('Successfully save evolution chain.'))

    def get_evolution_chain(self, id):
        response = urllib.request.urlopen(
            urllib.request.Request(
                self.url_evolution_chain.format(id=id),
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        )
        evol_chain = json.loads(response.read())
        request_pokemon_base = urllib.request.urlopen(
            urllib.request.Request(
                self.url_pokemon.format(name=evol_chain["chain"]["species"]["name"]),
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        )
        pokemon_base_json = json.loads(request_pokemon_base.read())
        if Pokemon.objects.filter(name=pokemon_base_json["name"]):
            raise CommandError("This evolution chain has already been loaded.")
        pokemon_base = Pokemon(id=pokemon_base_json["id"], name=pokemon_base_json["name"], height=pokemon_base_json["height"], weight=pokemon_base_json["weight"])
        pokemon_base.save()
        for stat_json in pokemon_base_json["stats"]:
            stat = Stat(name=stat_json["stat"]["name"], effort=stat_json["effort"], base_stat=stat_json["base_stat"], pokemon=pokemon_base)
            stat.save()
        if evol_chain["chain"]["evolves_to"]:
            self.get_evolves_to(pokemon_base, evol_chain["chain"]["evolves_to"])
        return

    def get_evolves_to(self, pokemon_base, evol_chain):
        for evolution in evol_chain:
            request_pokemon = urllib.request.urlopen(
                urllib.request.Request(
                    self.url_pokemon.format(name=evolution["species"]["name"]),
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
            )
            pokemon_json = json.loads(request_pokemon.read())
            pokemon = Pokemon(id=pokemon_json["id"], name=pokemon_json["name"], height=pokemon_json["height"], weight=pokemon_json["weight"])
            pokemon.save()
            for stat_json in pokemon_json["stats"]:
                stat = Stat(name=stat_json["stat"]["name"], effort=stat_json["effort"], base_stat=stat_json["base_stat"], pokemon=pokemon)
                stat.save()
            pokemon_base.evolution_to.add(pokemon)
            pokemon_base.save()
            if evolution["evolves_to"]:
                self.get_evolves_to(pokemon, evolution["evolves_to"])
        return
