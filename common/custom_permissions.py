from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class OnlyLoggedSuperuserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser