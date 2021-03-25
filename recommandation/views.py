from django.http.response import JsonResponse
from django.contrib.auth import login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from recommandation.serializers import AnimeSerializer, UserSerializer, RegisterSerializer
from recommandation.models import Anime

from rest_framework import generics, permissions,status
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
#Generix Vieaw API
from rest_framework import generics
from rest_framework import mixins
#authentification
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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

class AnimeList(APIView):
    def get(self, request):
        animes = Anime.objects.all()
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
        return Response({'message': 'L\'animé a été supprimé! Hmaza le BOSS'}, status=status.HTTP_204_NO_CONTENT)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

@api_view(['GET', 'POST'])
def anime_list(request):
    if request.method == 'GET':
        animes = Anime.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            animes = animes.filter(title__icontains=title)
        serializer = AnimeSerializer(animes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AnimeSerializer(data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET', 'PUT', 'DELETE'])
def anime_detail(request, pk):
    # find tutorial by pk
    try: 
        anime = Anime.objects.get(pk=pk) 
    except Anime.DoesNotExist: 
        return Response({'message': 'l\'Anime n\'existe pas'  }, status=status.HTTP_404_NOT_FOUND) 
 
    #Find a single Anime with an id
    if request.method == 'GET': 
        serializer = AnimeSerializer(anime) 
        return Response(serializer.data) 
    
    #Find a single Anime with an id
    elif request.method == 'PUT': 
        serializer = AnimeSerializer(anime, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a Anime with the specified id
    elif request.method == 'DELETE': 
        anime.delete() 
        return Response({'message': 'L\'animé a été supprimé! Hmaza le BOSS'}, status=status.HTTP_204_NO_CONTENT)