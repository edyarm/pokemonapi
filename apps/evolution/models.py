from django.db import models


class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()
    evolution_to = models.ManyToManyField('Pokemon', symmetrical=False, blank=True)


class Stat(models.Model):
    name = models.CharField(max_length=100)
    effort = models.IntegerField()
    base_stat = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, related_name='stats', on_delete=models.CASCADE)
