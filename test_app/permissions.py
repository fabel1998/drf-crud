from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
	"""Разрешение пользователям изменять свой профиль"""

	def has_object_permission(self, request, view, obj):
		"""Проверка может ли пользователь изменять свой профиль"""

		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.id == request.user.id


class PostOwnStatus(permissions.BasePermission):
	"""Разрешение исправлять свой собственный статус"""

	def has_object_permission(self, request, view, obj):
		"""Проверка пытается ли пользователь изменять свой статус"""

		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.user_profile.id == request.user.id 