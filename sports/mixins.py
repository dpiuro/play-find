from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class UserPermissionMixin:
    def has_permission(self, request, obj):
        return request.user.is_staff or obj.creator == request.user

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        obj = self.get_object()
        if not self.has_permission(request, obj):
            messages.error(
                request,
                "You do not have permission to perform this action."
            )
            return redirect(reverse("training-list"))
        return super().dispatch(request, *args, **kwargs)


class UserStatusMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = self.request.user.groups.filter(
            name="Admins"
        ).exists()
        context["is_staff"] = self.request.user.is_staff
        return context
