from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.mail import EmailMessage

from test_task.users.forms import Register
from test_task.users.models import CustomUser
from test_task.users.token import account_activation_token


class UsersView(ListView):
    """
    This class is responsible for displaying the list of users.
    """
    template_name = 'users/users.html'
    model = CustomUser
    context_object_name = 'user_list'
    ordering = 'id'


class UserRegister(SuccessMessageMixin, CreateView):
    """
    This class is responsible for displaying the new user registration page.
    """
    template_name = 'CRUD/create_update.html'
    model = CustomUser
    form_class = Register
    success_url = reverse_lazy('user_login')
    success_message = _('The user has been successfully registered')
    extra_context = {'header': _('Registration'), 'button_name': _('Register')}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return redirect(self.success_url)



class UserEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    This class is responsible for displaying the user data modification page.
    """
    template_name = 'CRUD/create_update.html'
    model = CustomUser
    form_class = Register
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'id'
    login_url = reverse_lazy('user_login')
    extra_context = {'header': _('Edit user'), 'button_name': _('To change')}

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = _('You dont have the rights to change another user')
            url = reverse_lazy('users')
        else:
            message = _('You are not logged in! Please log in')
            url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)

    def form_valid(self, form):
        form.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)
        messages.success(self.request, _('User successfully changed'))
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['user_id'] = str(user_id)
        return context

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

