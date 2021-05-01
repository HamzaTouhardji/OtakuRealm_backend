import datetime
import json
import datetime

from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from recommandation.serializers import AnimeSerializer, RecommandationSerializer, AnimeSerializerFilter, PrefererSerializer, ReviewSerializer,UtilisateurSerializer, UserSerializer, RegisterSerializer, GenreSerializer
from recommandation.models import Anime, Genre, Utilisateur, Recommandation, Preferer, Review

from rest_framework import generics, permissions,status, authentication, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class TopAnimeAllTime(APIView):
    def get(self, request):
        animes = Anime.objects.order_by('score').reverse()[:10]
        serializer = AnimeSerializerFilter(animes, many=True)
        return Response(serializer.data)

class TopAnimeSaison(APIView):
    def get(self, request):
        '''
        x = datetime.datetime.now()
        print(x.strftime("%m"))
        saison = 'Fall ' + str(x.year)
        '''
        animes = Anime.objects.filter(season = 'Spring 2021').order_by('score').reverse()[:10]
        serializer = AnimeSerializerFilter(animes, many=True)
        return Response(serializer.data)

class TopAnimeAnnee(APIView):
    def get(self, request):
        array = ['2021']
        regex = '^.*(%s).*$' % '|'.join(array)
        animes = Anime.objects.filter(season__iregex=regex).order_by('score').reverse()[:10]
        serializer = AnimeSerializerFilter(animes, many=True)
        return Response(serializer.data)

#######################################################################################

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

class UserAnimeList(APIView):
    def get(self, request):
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        review = Review.objects.filter(id_utilisateur = curent_utilisateur.id)
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)

        if not Review.objects.filter(id_anime=data["id_anime"], id_utilisateur=curent_utilisateur.id).exists():
            new_review = Review.objects.create(
                id_anime = Anime.objects.get(id = data["id_anime"]),
                id_utilisateur = Utilisateur.objects.get(id = curent_utilisateur.id),
                date = datetime.datetime.now(),
                score = data["score"],
                description = data["description"],
            )
            new_review.save()
            serializer = ReviewSerializer(new_review)

        return Response({
            'status': 'OK',
            'message': 'Ajout de la review.'
        }, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        Review.objects.filter(id_utilisateur=curent_utilisateur.id, id_anime=data["id_anime"]).update(score=data["score"])
        return Response({
            'message': 'Modification du score'
        }, status=status.HTTP_200_OK)
    
    def delete(self, request):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        Review.objects.filter(id_utilisateur=curent_utilisateur.id, id_anime=data["id_anime"]).delete()
        
        return Response(
            {
            'message': 'Suppression de la review'
        },status=status.HTTP_200_OK)

#######################################################################################

class RechercheListView(generics.ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

#######################################################################################

class GenreList(APIView):
    def get(self, request):
        genres = Genre.objects.all().order_by("name")
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserGenreList(APIView):
    def get(self, request):
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        genres_prefere = Preferer.objects.filter(id_utilisateur = curent_utilisateur.id)
        serializer = PrefererSerializer(genres_prefere, many=True)
        return Response(serializer.data)

    '''
    La fonction ajoute les genres aimes par l'utilisateur sans redondance  
    '''
    def post(self, request):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        for genre in data["genres"]:
            if not Preferer.objects.filter(id_genre=genre["id"], id_utilisateur=curent_utilisateur.id).exists():
                new_prefere = Preferer.objects.create(
                    id_utilisateur = Utilisateur.objects.get(id = curent_utilisateur.id),
                    id_genre = Genre.objects.get(id = genre["id"]),
                )
                new_prefere.save()
                serializer = PrefererSerializer(new_prefere)

        return Response({
            'status': 'OK',
            'message': 'Ajout des genres de utilisateur.'
        }, status=status.HTTP_200_OK)

    '''
    La fonction ajoute les genres et supprime les anciens  
    '''
    def put(self, request):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        Preferer.objects.filter(id_utilisateur=curent_utilisateur.id).delete()
        for genre in data["genres"]:
            if not Preferer.objects.filter(id_genre=genre["id"], id_utilisateur=curent_utilisateur.id).exists():
                new_prefere = Preferer.objects.create(
                    id_utilisateur = Utilisateur.objects.get(id = curent_utilisateur.id),
                    id_genre = Genre.objects.get(id = genre["id"]),
                )
                new_prefere.save()
                serializer = PrefererSerializer(new_prefere)

        return Response({
            'status': 'Bad request',
            'message': 'Ajout des genres de utilisateur. (avec suppression des anciens)'
        }, status=status.HTTP_200_OK)

#######################################################################################
from rest_framework.renderers import JSONRenderer
class UtilisateurViewSet(ModelViewSet):
    serializer_class = UtilisateurSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.id
        u = User.objects.get(id = user_id)
        user = Utilisateur.objects.filter(user=user_id)
        return user

    
    def create(self, request, *args, **kwargs):
        data = request.data

        new_utilisateur = Utilisateur.objects.create( 
            user = User.objects.get(id=self.request.user.id),           
            bio = data["bio"], 
            photo_de_profil = data['photo_de_profil'], 
            sexe = data['sexe'], 
            age = data['age'], 
        )
                
        new_utilisateur.save()
        serializer = UtilisateurSerializer(new_utilisateur)
        
        
        if serializer.is_valid():
            return Response(serializer.data)
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request, *args, **kwargs):
        put_utilisateur = Utilisateur.objects.get(user=self.request.user.id)

        data = request.data

        put_utilisateur.user = User.objects.get(id=self.request.user.id)
        put_utilisateur.bio = data["bio"] 
        put_utilisateur.photo_de_profil = data["photo_de_profil"] 
        put_utilisateur.sexe = data["sexe"] 
        put_utilisateur.age = data["age"] 

        put_utilisateur.save()
        serializer = UtilisateurSerializer(put_utilisateur)

        return Response({
                'message': 'Utilisateur modifié'
            }, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        patch_utilisateur = Utilisateur.objects.get(user=self.request.user.id)
        data = request.data

        patch_utilisateur.user = User.objects.get(id=self.request.user.id)
        patch_utilisateur.bio = data.get("bio", patch_utilisateur.bio) 
        patch_utilisateur.photo_de_profil = data.get("photo_de_profil", patch_utilisateur.photo_de_profil) 
        patch_utilisateur.sexe = data.get("sexe", patch_utilisateur.sexe) 
        patch_utilisateur.age = data.get("age", patch_utilisateur.age) 

        patch_utilisateur.save()
        serializer = UtilisateurSerializer(patch_utilisateur)

        return Response({
                'message': 'Utilisateur patché'
            }, status=status.HTTP_200_OK)

class RecommandationViewSet(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommandationSerializer
    queryset = Recommandation.objects.all()
    
    def get_queryset(self):
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        return Recommandation.objects.filter(id_utilisateur = curent_utilisateur.id)
    
    def create(self, request, *args, **kwargs):
        data = request.data

        new_recommandation = Recommandation.objects.create(            
            id_utilisateur = Utilisateur.objects.get(user=self.request.user.id),
            id_anime = Anime.objects.get(id=data["id_anime"]),
            score = data["score"]
        )
                
        new_recommandation.save()
        serializer = RecommandationSerializer(new_recommandation)
        
       
        if serializer.is_valid:
            return Response(serializer.data)
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        curent_utilisateur = Utilisateur.objects.get(user = self.request.user.id)
        Recommandation.objects.filter(id_utilisateur=curent_utilisateur.id, id_anime=data["id_anime"]).update(score=data["score"])
        return Response({
            'message': 'Modification de la recommandation'
        }, status=status.HTTP_200_OK)

#######################################################################################

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

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        new_utilisateur = Utilisateur.objects.create( 
            user = User.objects.get(id=user.id),           
            bio = "", 
            photo_de_profil = "https://journalmetro.com/wp-content/uploads/2017/04/default_profile_400x400.png?w=860", 
            sexe = "", 
            age = None, 
        )
                
        new_utilisateur.save()
        serializer = UtilisateurSerializer(new_utilisateur)
        
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

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=204)