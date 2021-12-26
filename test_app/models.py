from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
	"""Помогает работать с нашей пользовательской моделью"""

	def create_user(self, email, name, password=None):
		"""Создаем нового пользователя"""

		if not email:
			raise ValueError('У пользователя должен быть адрес электронной почты')

		email = self.normalize_email(email)
		user = self.model(email=email, name=name)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, name, password):
		"""Создание супер пользователя"""

		user = self.create_user(email, name, password)

		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)

		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
	"""Таблица пользователя"""

	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def get_full_name(self):
		"""Получения полного имени пользователя"""

		return self.name

	def get_short_name(self):
		"""Получения короткого имена пользователя"""

		return self.name

	def __str__(self):
		"""Возврат объекта в виде строки"""

		return self.email


class ProfileFeedItem(models.Model):
	"""Обновление статуса пользователя"""

	user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	status_text = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""Возврат объекта в виде строки"""
		return self.status_text