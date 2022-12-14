from django.db  import models

class User(models.Model):
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=25)
  bio = models.CharField(max_length=400)
  profile_image_url = models.CharField(max_length=200)
  email = models.EmailField(max_length=254) 
  created_on = models.DateField()
  active = models.BooleanField(default=False)
