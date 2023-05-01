from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class IndexView(TemplateView):
    """
    This class is responsible for displaying the home page of the application.
    """
    template_name = 'index.html'


class UserLogin(SuccessMessageMixin, LoginView):
    """
    This class is responsible for displaying the Login page .
    """
    template_name = 'user_login.html'
    success_message = _('You are logged in')


class UserLogout(SuccessMessageMixin, LogoutView):
    """
    This class is responsible for displaying the Logout page .
    """
    def dispatch(self, request, *args, **kwargs):
        """
        This method outputs a flash message about successful Logout.
        """
        messages.success(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
