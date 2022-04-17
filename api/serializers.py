from dataclasses import field
from rest_framework import serializers
from .models import *

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['Name', 'HKU_ID']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['Venue_Code']

class AccessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRecord
        fields = '__all__'