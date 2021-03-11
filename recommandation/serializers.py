from rest_framework import serializers
from.models import Anime, Genre
from django.contrib.auth.models import User
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

# Genre Serializer
class GenreSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user