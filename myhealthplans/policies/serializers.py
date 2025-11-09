from rest_framework import serializers
from .models import Policy

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'



class PolicySerializerDetails(serializers.ModelSerializer):
    # Custom date formatting
    dob = serializers.DateField(format="%d-%b-%Y", read_only=True)
    start_date = serializers.DateField(format="%d-%b-%Y", read_only=True)
    end_date = serializers.DateField(format="%d-%b-%Y", read_only=True)

    class Meta:
        model = Policy
        fields = "__all__"

class PolicyEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"