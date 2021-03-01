from rest_framework import serializers

from .models import Manga

class RecommandationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manga
        fields = ('id', 'title', 'picture')