from rest_framework import serializers
from.models import Anime, Genre, Utilisateur, Recommandation
from django.contrib.auth.models import User
#from django.contrib.auth.models import User
#from rest_framework.authtoken.models import Token

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'
        #extra_kwargs = {'URL': {'required':True}}

# Utilisateur Serializer
class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'
        depth = 1

# Genre Serializer
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'

# Recommandation Serializer
class RecommandationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Recommandation
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
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password']
        )

        return user