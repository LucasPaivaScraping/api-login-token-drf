from rest_framework import serializers
from .models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    """
    Persona serializer
    """
    class Meta:
        model = Persona
        fields = (
            'id',
            'nombre',
            'apellido',
        )
