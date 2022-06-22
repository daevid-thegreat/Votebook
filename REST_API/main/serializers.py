from rest_framework import serializers

from .models import *


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['id','party_name']
