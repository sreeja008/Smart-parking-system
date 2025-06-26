from django.db import models

# Create your models here.

class User_details(models.Model):
    User_id = models.AutoField(primary_key = True)
    Email = models.EmailField(max_length = 50)
    Password = models.CharField(max_length = 15, null = True)

    class Meta:
        db_table = 'user_details'

class Upload_File(models.Model):
    Video_Id = models.AutoField(primary_key=True)
    Video = models.FileField(upload_to='videos/') 

    class Meta:
        db_table = 'upload_video'