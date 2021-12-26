from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions



class HelloApiView(APIView):
	"""Тестовое представление АПИ"""

	serializer_class = serializers.HelloSerializer

	def get(self, request, format=None):
		"""Возвращает список"""

		an_apiview = [
			'Использует HTTP методы функции (get, post, patch, put, delete)',
			'Это как традиционное представление Django',
			'Только с большим контролем логики нашего приложения',
			'Cопоставляется вручную с URL-адресами'
		]

		return Response({'message': 'Hello!', 'an_apiview': an_apiview})

	def post(self, request):
		"""Создаем приветственное сообщение"""

		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name = serializer.data.get('name')
			message = f'Hello {name}'

			return Response({'message': message})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def put(self, request, pk=None):
		"""Обновляет объект"""

		return Response({'method': 'put'})

	def patch(self, request, pk=None):
		"""Исправление только указанные в запросе поля объекта"""

		return Response({'method': 'patch'})

	def delete(self, request, pk=None):
		"""Удаляет объект"""

		return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
	"""Тест АПИ вьюсетс"""

	serializer_class = serializers.HelloSerializer

	def list(self, request):
		"""Возвращает приветственное сообщение"""

		a_viewset = [
			'Можно использовать(list, create, retrieve, update, partialupdate, destroy',
			'Авто подставление URL с помощью маршрутов',
			'Большая функциональность с наименьшим кодом'
		]

		return Response({'message': 'Hello', 'a_viewset': a_viewset})

	def create(self, request):
		"""Создание нового объекта"""

		serializer = serializers.HelloSerializer(data=request.data)

		if serializer.is_valid():
			name = serializer.data.get('name')
			message = f'Hello {name}'
			return Response({'message':message})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		"""Получение объекта по его индетификатору"""

		return Response({'http_method':'GET'})

	def update(self, request, pk=None):
		"""Обновление объекта в базе данных"""

		return Response({'http_method':'PUT'})

	def partial_update(self, request, pk=None):
		"""Частичное обновление объекта в базе данных"""

		return Response({'http_method':'PATCH'})

	def destroy(self, request, pk=None):
		"""Удаление объекта из базы данных"""

		return Response({'http_method':'DELETE'})
	
class UserProfileViewSet(viewsets.ModelViewSet):
	"""Чтение, Создание, Обновление пользователей"""

	serializer_class = serializers.UserProfileSerializer
	queryset = models.UserProfile.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdateOwnProfile,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
	"""Проверяет логи и пароль и возвращает токен авторизации"""

	serializer_class = AuthTokenSerializer
	
	def create(self, request):
		"""Использует ObtainToken для проверки и создания токена"""

		return ObtainAuthToken().as_view()(request=request._request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
	"""Создание, обновление, чтение элементов статуса"""

	authentication_classes = (TokenAuthentication,)
	serializer_class = serializers.ProfileFeedItemSerializer
	queryset = models.ProfileFeedItem.objects.all()
	permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

	def perform_create(self, serializer):
		"""Устанавливает пользователя вошедшего в систему"""

		serializer.save(user_profile=self.request.user)