from rest_framework import serializers
from .models import Users

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "username",
            "email_address",
            "password",
            "name",
        
        ]
        
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self,validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    