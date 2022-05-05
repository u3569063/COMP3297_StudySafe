from dataclasses import field
from rest_framework import serializers
from .models import *

class CloseContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['Name', 'HKU_ID']

class DisinfectVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['Venue_Code']

class AccessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRecord
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'