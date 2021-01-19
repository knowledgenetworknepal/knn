


from django.core.exceptions import PermissionDenied


# this checks if the user is in group Admin or not
class IsAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Admin').exists():
                return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

