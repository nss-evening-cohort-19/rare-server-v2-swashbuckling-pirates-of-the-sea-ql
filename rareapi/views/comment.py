from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, User, Post

class CommentView(ViewSet):
  """Comment view"""
  
  def retrieve(self, request, pk):
    try:
      comment = Comment.objects.get(pk=pk)
      serializer = CommentSerializer(comment)
      return Response(serializer.data)
    except Comment.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    comments = Comment.objects.all()
    post = request.query_params.get('post', None)
    if post is not None:
      comments = comments.filter(post_id=post)
      
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    author = User.objects.get(id=request.data["author_id"])
    post = Post.objects.get(pk=request.data["post_id"])
    
    comment = Comment.objects.create(
      post_id=post,
      author_id=author,
      content=request.data["content"],
      created_on=request.data["created_on"]
    )
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
  
  def update(self, request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.content = request.data["content"]
    comment.created_on = request.data["created_on"]
    comment.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommentSerializer(serializers.ModelSerializer):
  """serializer for comments"""
  
  class Meta:
    model = Comment
    depth = 1
    fields = ('id', 'post_id', 'author_id', 'content', 'created_on')