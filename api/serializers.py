from dataclasses import field
from rest_framework import serializers
from .models import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class AccessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRecord
        fields = '__all__'