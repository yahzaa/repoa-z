from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
#from rest_framework import viewset
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
# Create your views here.
from . import permissions

class HelloWorldView(APIView):
	"""Test API View"""

	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):

		an_apiview = [
			'Uses HTTP methods as function (get, post, patch, put, delte',
			'It is similar to a traditional Django View',
			'Gives you the most control over your logic',
			'Is mapped manually to URLs',
			]

		return Response({'message':'Hello!', 'an_apiview':an_apiview})

	def post(self, request):
		"""Create a hello message with our name"""

		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name=serializer.data.get('name')
			message= "hello {0}".format(name)
			return Response({'message':message})
		else:
			return Response(
				serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
	def put(self, request, pk=None):
		"""Handles updating an object"""
		return Response({'method':'put'})

	def patch(self, request, pk=None):
		"""patch request, only updates fields provided in the request"""
		return Response({'method':'patch'})

class HelloWorldViewSet(viewsets.ViewSet):
	"""Test Viewset Function"""

	serializer_class = serializers.HelloSerializer

	def list(self, request):
		"""return a hello message"""

		a_viewset =['Users actions',
		'automatically maps to urls',
		'provides more functional']

		return Response({'message':'Hello!', 'a_viewset':'ya-digg'})

	def create(self, request):
		"""Create a new hello message"""

		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name = serializer.data.get('name')
			message = 'Hello {0}'.format(name)
			return Response({'message' : message})
		else: 
			return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def retrieve(self, request, pk=None):
		"""Hanldes getting an object its ID"""

		return Response({'http_method': "GET"})

	def update(self, request, pk=None):
		"""Handles updating an object"""

		return Response({'http_method': 'PUT'})

	def partial_update(self,request, pk=None):
		"""Handles updating part of an object"""

		return Response({'http_method': 'Patch'})

	def destroy(self, request, pk=None):
		"""Handles removing an object"""

		return Response({'http_method': "Delete"})

# class AthleteProfileViewSet(views.ModelViewSet):
# 	"""Handles creating, profiles"""

# 	serializer_class = serializers.AthleteProfileSerializer
# 	queryset = models.AthleteProfile.objects.all()

class AthleteProfileViewSet(viewsets.ModelViewSet):
	"""handles creating, and updating profiles"""

	serializer_class = serializers.AthleteProfileSerializer
	queryset = models.AthleteProfile.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name','email',)

class AthleteFeedViewSet(viewsets.ModelViewSet):
	"""handles creating, reading, and updating profile feed items."""

	serializer_class = serializers.AthleteFeedItemSerializer
	queryset = models.AthleteFeedItem.objects.all()

	def perform_create(self, serializer):
		"""sets the user profile to the logged in user."""

		serializer.save(user_profile=self.request.user)

class AthleteEmgData(viewsets.ModelViewSet):
	"""handles listing out the viewset data, creating, and destroying emg"""

	serializer_class = serializers.AthleteEMGDataSerializer
	queryset = models.AthleteEMGDataItem.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ('user_profile',)

	def perform_create(self, serializer):
		"""sets the user profile to the logged in user."""

		serializer.save(user_profile=self.request.user)


class AthleteMedSessionData(viewsets.ModelViewSet):
	"""handles listing out the viewset of the emg results"""

	serializer_class = serializers.AthleteMedSessionSerializer
	queryset = models.AthleteMedSession.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ('user_profile',)
	permission_class = (permissions.UpdateOwnProfile)
	authentication_classes = (TokenAuthentication,)

	
	def perform_create(self, serializer):
		"""sets the user profile to the logged in user."""

		serializer.save(user_profile=self.request.user)


class LoginViewSet(viewsets.ViewSet):
	"""Checks email and password and returns auth token"""

	serializer_class = AuthTokenSerializer

	def create(self, request):
		"""Use the obtainAuthToken APIView to validate and create a token"""

		return ObtainAuthToken().post(request)

class Player(viewsets.ModelViewSet):
	"""view set for viewing the player profile data"""

	serializer_class = serializers.Player
	queryset = models.Player.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdatePlayerProfile, IsAuthenticatedOrReadOnly)


	def perform_create(self, serializer):
		"""sets the user profile to the logged in user."""

		serializer.save(trainer_profile=self.request.user)

class Team(viewsets.ModelViewSet):
	""" creates the different teams"""

	serializer_class = serializers.Team
	queryset = models.Team.objects.all()

class Session(viewsets.ModelViewSet):
	"""creates a session for the athlete"""

	serializer_class = serializers.Session
	queryset = models.Session.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdatePlayerSession, IsAuthenticatedOrReadOnly)

	def perform_create(self, serializer):
		"""sets the serializer to the correct profile"""

		serializer.save(trainer_profile=self.request.user)