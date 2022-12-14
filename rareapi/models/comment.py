from django.db import models
from .user import User
from .post import Post

class Comment(models.Model):
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  author_id = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField(max_length=800)
  created_on = models.DateTimeField(auto_now_add=True)
