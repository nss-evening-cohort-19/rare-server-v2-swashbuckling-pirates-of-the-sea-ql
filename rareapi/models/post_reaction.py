from django.db import models
from .user import User
from .reaction import Reaction
from .post import Post

class PostReaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
