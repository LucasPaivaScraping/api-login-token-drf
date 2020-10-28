from django.shortcuts import render
from rest_framework import generics
# Requried to login form
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache  # Last django version
from django.views.decorators.csrf import csrf_protect  # Last django version
from django.views.generic.edit import FormView  # Last django version

from django.contrib.auth import login, logout, authenticate  # Very important to login and authenticate

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# End requirements login form

from .models import Persona
from .serializers import PersonaSerializer


# Class for list personas
class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = (IsAuthenticated, )
    authentication_class = (TokenAuthentication, )  # Its different from authentication_classes


# Vista que renderiza el form de login
class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:persona_list')

    @method_decorator(csrf_protect)
    #@method_decorator(never_cache())
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        token, _ = Token.objects.get_or_create(user=user)  # aca creo un token relacionado al usuario
        if token:
            login(self.request, user)
            return super(Login, self).form_valid(form)


class Logout(APIView):

    def get(self, request):
        request.user.auth_token.delete() # Elimino el toquen del usuario
        logout(request) # me deslogueo
        return Response(status=status.HTTP_200_OK)
