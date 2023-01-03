from django.db import models
from .user import User
from .category import Category
from django.forms.models import model_to_dict

class Post(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  publication_date = models.DateField()
  image_url = models.CharField(max_length=255)
  content = models.TextField(max_length=1000)
  
  @property
  def reactions_on_posts(self):
    return self.__reactions_on_posts
  
  @reactions_on_posts.setter
  def reactions_on_posts(self, value):
    self.__reactions_on_posts = value
    
