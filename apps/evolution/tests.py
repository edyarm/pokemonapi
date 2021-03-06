from django.core.management import call_command
from django.test import TestCase

from .models import Pokemon


class PokemonModelTests(TestCase):

    def test_command_many_evolutions(self):
        args = [67]
        opts = {}
        call_command('getevolutionchain', *args, **opts)
        evolutions = list(Pokemon.objects.filter(name="eevee"))
        self.assertIs(len(evolutions) > 0, True)
