from django.db import models

# Create your models here.
class employee(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(null=True,unique=True)
    password=models.CharField(max_length=255)
    punch_in=models.DateTimeField(null=True)
    punch_out=models.DateTimeField(null=True)
    durations=models.IntegerField(null=True)

    