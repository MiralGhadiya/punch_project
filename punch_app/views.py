from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response  import Response
from rest_framework.views import APIView 
from rest_framework import status
from .models import employee
from .serializer import EmployeeSerializer,punchserializer
import datetime
from pytz import timezone
from passlib.context import CryptContext
# from django.db.models import Q
pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
import datetime

from cryptography.fernet import Fernet
# import base64
# Create your views here.
class registerview(APIView):
    # def get(self,request):
    #     obj=employee.objects.all()
    #     serializer=EmployeeSerializer(obj, many=True)
    #     return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        obj_data=request.data
        obj_data['password']=pwd_context.hash(obj_data['password'])
        print(obj_data['password'])
        print(obj_data)
        serializer=EmployeeSerializer(data=obj_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class loginview(APIView):

    def post(self,request):
        obj_data=request.data
        email=obj_data['email']
        password=obj_data['password']
        # print(email)
        # print(password)
        try:

            employee_obj=employee.objects.get(email=email)
        except employee.DoesNotExist:
            # print(employee_obj)
            return Response({"message":"email  invalid"},status=status.HTTP_400_BAD_REQUEST)
        #hashed_password = employee_obj[0].password

        if employee_obj:
            if pwd_context.verify(password,employee_obj.password):

                    return Response({"message":"login successful"},status=status.HTTP_200_OK)
            else:
                    
                    return Response({"message":"password is not matched"},status=status.HTTP_400_BAD_REQUEST)
  
class PunchInView(APIView):
    def get(self,request,id):
        try:
            obj=employee.objects.get(id=id)
        except employee.DoesNotExist:
            msg={"msg":"not found"}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)
            
        serialiser=punchserializer(obj)
        return Response(serialiser.data,status=status.HTTP_200_OK)
    
    def post(self, request,id):
        obj_data=request.data 
        
       
        try:
            employee_obj=employee.objects.get(id=id)
            # print(employee_obj,"0"*100)
            if employee_obj:
                if employee_obj.punch_in and employee_obj.punch_in.date() == datetime.datetime.now().date():
                    return Response({"message": "You are already punched in for today."}, status=status.HTTP_400_BAD_REQUEST)
                punch_in_time = datetime.datetime.now()
                employee_obj.punch_in = punch_in_time
                employee_obj.save()
                return Response({"message":"punch in successfully"},status=status.HTTP_200_OK)
            else:
                return Response("id does not exits")
        except employee.DoesNotExist as e:
                
            return Response("user not found")
        
 
  


        
        




class PunchOutView(APIView):
    def post(self, request,id):
        obj_data = request.data 
        try:
            employee_obj=employee.objects.get(id=id)
            # print(employee_obj,"0"*100)
            if employee_obj:
                if employee_obj.punch_out and employee_obj.punch_out.date() == datetime.datetime.now().date():
                    return Response({"message": "You are already punched out for today."}, status=status.HTTP_400_BAD_REQUEST)
                punch_out_time = datetime.datetime.now()
                employee_obj.punch_out = punch_out_time
                employee_obj.save()
                duration = employee_obj.punch_out.replace(tzinfo=None) - employee_obj.punch_in.replace(tzinfo=None)
                hours = duration.total_seconds() / 3600
                rounded_hours = round(hours)
                employee_obj.durations = rounded_hours
                # print(duration,"()")
                # import time;time.sleep(101010)
                employee_obj.save()
                return Response({"message": f"Punch-out successful. Hours worked today: {(rounded_hours)}"}, status=status.HTTP_200_OK)
    
            else:
                return Response("id does not exits")
        except employee.DoesNotExist as e:
                
            return Response("user not found")

        # Validate input data
       

    






