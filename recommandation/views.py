import datetime

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
from django.shortcuts import get_object_or_404
from rest_framework import filters

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
        animes = Anime.objects.order_by('score').reverse()[:10]
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

class TopAnimeSaison(APIView):
    def get(self, request):
        '''
        x = datetime.datetime.now()
        print(x.strftime("%m"))
        saison = 'Fall ' + str(x.year)
        '''
        animes = Anime.objects.filter(season = 'Spring 2021').order_by('score').reverse()[:10]
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

class TopAnimeAnnee(APIView):
    def get(self, request):
        array = ['2021']
        regex = '^.*(%s).*$' % '|'.join(array)
        animes = Anime.objects.filter(season__iregex=regex).order_by('score').reverse()[:10]
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

class RechercheListView(generics.ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

class RechercheViewSet(ModelViewSet):
    serializer_class = AnimeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        data = request.data
        o = Anime.objects.filter(title__icontains=data["recherche"])
        return o
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

#######################################################################################

class UserList(APIView):
    def get(self, request):
        users = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(users, many=True)
        return Response(serializer.data)

class UtilisateurViewSet(ModelViewSet):
    serializer_class = UtilisateurSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.id
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

        for anime in data["animes"]:
            anime_obj = Anime.objects.get(id=anime["id"])
            new_utilisateur.animes.add(anime_obj)
        
        for genre in data["genres"]:
            genre_obj = get_object_or_404(Genre, id=genre["id"])
            #genre_obj = Genre.objects.get(id=genre["id"])
            new_utilisateur.genres.add(anime_obj)

        new_utilisateur.save()
        serializer = UtilisateurSerializer(new_utilisateur)

        if serializer.is_valid():
            serializer = UtilisateurSerializer(new_utilisateur)
            return Response(serializer.data)
        '''
            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)
        '''

    def put(self, request, *args, **kwargs):
        put_utilisateur = Utilisateur.objects.get(user=self.request.user.id)

        data = request.data

        put_utilisateur.user = User.objects.get(id=self.request.user.id)
        put_utilisateur.bio = data["bio"] 
        put_utilisateur.photo_de_profil = data["photo_de_profil"] 
        put_utilisateur.sexe = data["sexe"] 
        put_utilisateur.age = data["age"] 
        
        for anime in data["animes"]:
            anime_obj = Anime.objects.get(id=anime["id"])
            put_utilisateur.animes.add(anime_obj)
        
        for genre in data["genres"]:
            genre_obj = Genre.objects.get(id=genre["id"])
            put_utilisateur.genres.add(genre_obj)

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

        for anime in data["animes"]:
            anime_obj = get_object_or_404(Anime, id=anime["id"])
            anime_obj = Anime.objects.get(id=anime["id"])
            patch_utilisateur.animes.add(anime_obj)
        
        for genre in data["genres"]:
            genre_obj = Genre.objects.get(id=genre["id"])
            patch_utilisateur.genres.add(genre_obj)

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
        user = self.request.user.id
        return Recommandation.objects.filter(id_utilisateur = user)

class InfoUser(APIView):
    serializer_class = UtilisateurSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def get(self, request):
        user_id = self.request.user.id
        user = Utilisateur.objects.filter(user=user_id)
        serializer = UtilisateurSerializer(user, many=True)
        return Response(serializer.data)
    
    def post(self, request):
            serializer = UtilisateurSerializer(data=request.data )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeDetailAPIView(APIView):
  #permission_classes = (,)
  serializer_class = UtilisateurSerializer
  queryset = Utilisateur.objects.all()

  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)

  def update(self, serializer):
    serializer.save(updated_by_user=self.request.user)

@api_view(['PUT'])
def snippet_detail(request, pk):
    try:
        snippet = Utilisateur.objects.get(id=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UtilisateurSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=204)