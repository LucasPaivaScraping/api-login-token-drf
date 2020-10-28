from django.urls import path
from .views import PersonaList

urlpatterns = [
    path('persona/', PersonaList.as_view(), name='persona_list'),
    path('tuvieja/', PersonaList.as_view(), name='tuvieja'),
]
