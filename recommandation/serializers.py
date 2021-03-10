from rest_framework import serializers
from.models import Anime, User, Genre
#from django.contrib.auth.models import User
#from rest_framework.authtoken.models import Token

class RecommandationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Anime
        fields = (
            'id', 
            'title', 
            'season', 
            'score', 
            'production_studio', 
            'number_of_episodes', 
            'episode_duration', 
            'synopsis', 
            'rating', 
            'URL'  )
        #fields = '__all__'
        #extra_kwargs = {'URL': {'required':True}}

class GenreSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'