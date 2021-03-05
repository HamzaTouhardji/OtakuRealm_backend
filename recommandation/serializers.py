from rest_framework import serializers

from .models import Anime

class RecommandationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Anime
        fields = ('id', 'title', 'picture')