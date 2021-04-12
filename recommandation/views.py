from django.http.response import JsonResponse
from django.contrib.auth import login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from recommandation.serializers import AnimeSerializer, RecommandationSerializer, UtilisateurSerializer, UserSerializer, RegisterSerializer, GenreSerializer
from recommandation.models import Anime, Genre, Utilisateur, Recommandation

from rest_framework import generics, permissions,status
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
#Generix Vieaw API
from rest_framework import generics
from rest_framework import mixins
#authentification
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

#ListUsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

#CustomAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class GenericAPIView(generics.GenericAPIView, 
        mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin):

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'id'

    def get(self, request, id = None):
        if id: 
            return self.retrieve(request)
        else: 
            return self.list(request)

    def put(self, request, id=None):
        return self.update(request, id)
    
    def post(self, request, id=None):
        return self.create(request)
        
    def delete(self, request, id):
        return self.destroy(request, id)


class TopAnimeAllTime(APIView):
    def get(self, request):
        animes = Anime.objects.order_by('score').reverse()[:20]
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

import datetime
class TopAnimeSaison(APIView):
    def get(self, request):
        '''
        x = datetime.datetime.now()
        print(x.strftime("%m"))
        saison = 'Fall ' + str(x.year)
        '''
        animes = Anime.objects.filter(season = 'Spring 2020')[:20]
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

class AnimeList(APIView):
    def get(self, request):
        animes = Anime.objects.all()[:20]
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnimeSerializer(data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnimeDetails(APIView):
    def get_object(self, id):
        # find tutorial by pk
        try: 
            return Anime.objects.get(id=id) 
        except Anime.DoesNotExist: 
            return Response({'message': 'l\'Anime n\'existe pas'  }, status=status.HTTP_404_NOT_FOUND) 
    
    def get(self, request, id):
        anime = self.get_object(id)
        serializer = AnimeSerializer(anime) 
        return Response(serializer.data) 
    
    #Find a single Anime with an id
    def put(self, request, id):
        anime = self.get_object(id)
        serializer = AnimeSerializer(anime, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a Anime with the specified id
    def delete(self, request, id):
        anime = self.get_object(id)
        anime.delete() 
        return Response({'message': 'L\'animé a été supprimé!'}, status=status.HTTP_204_NO_CONTENT)

#######################################################################################

class GenreList(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#######################################################################################

class UserList(APIView):
    def get(self, request):
        users = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(users, many=True)
        return Response(serializer.data)

class UtilisateurViewSet (ModelViewSet):
    serializer_class = UtilisateurSerializer
    queryset = Utilisateur.objects.all()

class RecommandationViewSet(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommandationSerializer
    queryset = Recommandation.objects.all()
    
    def get_queryset(self):
        user = self.request.user.id
        return Recommandation.objects.filter(id_utilisateur = user)


class InfoUser(generics.ListAPIView):
    serializer_class = UtilisateurSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Utilisateur.objects.filter(user=user_id)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

#######################################################################################

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })