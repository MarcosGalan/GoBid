from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.forms import forms
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from access.forms import CustomUserCreationForm, CustomUserChangeForm, ChangePasswordForm
from core.models import CustomUser


class AccessView(View):
    template_name = 'access/access.html'

    def get(self, request, *args, **kwargs):
        login_form = AuthenticationForm()
        register_form = CustomUserCreationForm()
        return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})

    def post(self, request, *args, **kwargs):
        # Manejar el formulario de inicio de sesión
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('profile')  # Reemplaza 'home' con el nombre de la vista de inicio de tu aplicación
            else:
                register_form = UserCreationForm()
                return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})

        # Manejar el formulario de registro
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()

                # Añadir el usuario al grupo 'Usuarios' (o el nombre del grupo que desees)
                user_group = Group.objects.get(name='users')  # Asegúrate de cambiar esto al nombre de tu grupo
                user.groups.add(user_group)

                login(request, user)

                return redirect('home')  # Reemplaza 'home' con el nombre de la vista de inicio de tu aplicación
            else:
                # Si no es ni login ni register, mostrar ambos formularios
                login_form = AuthenticationForm()
                return render(request, self.template_name, {'login_form': login_form, 'register_form': register_form})


class Logout(LogoutView):
    template_name = 'core/home.html'


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile/profile.html'
    login_url = 'access'

    def get(self, request):
        user = request.user
        form = CustomUserChangeForm(instance=user)

        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request):
        user = request.user
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile') + '?success')
        else:
            return render(request, self.template_name, {'user': user, 'form': form})


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'profile/change_password.html'  # Create a template for this view
    success_url = reverse_lazy('profile')
