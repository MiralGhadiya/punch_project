from rest_framework import serializers
from .models import employee
from django.http import JsonResponse
from rest_framework import status

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ('id','name', 'email','password')

class punchserializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ('id','name', 'email','password','punch_in')

        extra_kwargs = {
            'punch_in': {
                'write_only': True
            }
        }

        # def create(self, validated_data):
        #     user = employee(
        #         email=validated_data['email'],
        #         username=validated_data['username']
        #     )
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return JsonResponse(user,
        #                 safe=False, status=status.HTTP_200_OK)