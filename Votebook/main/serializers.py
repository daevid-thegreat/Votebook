from rest_framework import serializers

from .models import *


class subjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id','subject_name','subject_description']
        
