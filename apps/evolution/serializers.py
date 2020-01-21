from rest_framework import serializers
from .models import Pokemon, Stat


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('name', 'effort', 'base_stat')
        ordering = ('name', 'effort', 'base_stat')


class EvolutonSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'type': instance.type,
            'name': instance.name,
            'id': instance.id
        }


class PokemonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    stats = StatSerializer(many=True)
    evolutions = EvolutonSerializer(many=True)
