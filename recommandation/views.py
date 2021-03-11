from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from recommandation.models import Anime
from recommandation.serializers import RecommandationSerializer, UserSerializer, RegisterSerializer
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
    
from rest_framework import generics, permissions
from knox.models import AuthToken
from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

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

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

@api_view(['GET', 'POST', 'DELETE'])
def recommandation_list(request):
    if request.method == 'GET':
        animes = Anime.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            animes = animes.filter(title__icontains=title)
        
        recommandation_serializer = RecommandationSerializer(animes, many=True)
        return JsonResponse(recommandation_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        recommandation_data = JSONParser().parse(request)
        recommandation_serializer = RecommandationSerializer(data=recommandation_data)
        if recommandation_serializer.is_valid():
            recommandation_serializer.save()
            return JsonResponse(recommandation_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(recommandation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET', 'PUT', 'DELETE'])
def recommandation_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        anime = Anime.objects.get(pk=pk) 
    except Anime.DoesNotExist: 
        return JsonResponse({'message': 'l\'Anime n\'exist pas'  }, status=status.HTTP_404_NOT_FOUND) 
 
    #Find a single Anime with an id
    if request.method == 'GET': 
        recommandation_serializer = RecommandationSerializer(anime) 
        return JsonResponse(recommandation_serializer.data) 
    
    #Find a single Anime with an id
    elif request.method == 'PUT': 
        anime_data = JSONParser().parse(request) 
        recommandation_serializer = RecommandationSerializer(anime, data=anime_data) 
        if recommandation_serializer.is_valid(): 
            recommandation_serializer.save() 
            return JsonResponse(recommandation_serializer.data) 
        return JsonResponse(recommandation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete a Anime with the specified id
    elif request.method == 'DELETE': 
        anime.delete() 
        return JsonResponse({'message': 'L\'animé a été supprimé!'}, status=status.HTTP_204_NO_CONTENT)
        
    #Delete all animes from the database
    elif request.method == 'DELETE':
        count = Anime.objects.all().delete()
        return JsonResponse({'message': '{} Animes were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
