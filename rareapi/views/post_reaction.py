from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import PostReaction, User, Reaction, Post

class PostReactionSerializer(serializers.ModelSerializer):
  class Meta:
      model = PostReaction
      fields = ('id', 'user', 'reaction', 'post')
      depth = 2

class PostReactionView(ViewSet):
  """ ViewSet for PostReaction Requests"""
  def list(self, request):
    """Handle GET requests for PostReactions"""
    post_reactions = PostReaction.objects.all()
    
    serializer = PostReactionSerializer(post_reactions, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    """Handle Requests for GET single post reaction"""
    try:
      post_reaction = PostReaction.objects.get(pk=pk)
      serializer = PostReactionSerializer(post_reaction)
      return Response(serializer.data)
    except PostReaction.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

  def create(self, request):
    """Handle POST requests to post reaction"""
    user = User.objects.get(id=request.data["user_id"])
    reaction = Reaction.objects.get(id=request.data["reaction_id"])
    post = Post.objects.get(id=request.data["post_id"])
    post_reaction = PostReaction.objects.create(
      user = user,
      reaction = reaction,
      post = post
    )
    serializer = PostReactionSerializer(post_reaction)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for post reaction"""
    post_reaction = PostReaction.objects.get(pk=pk)
    post_reaction.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    """Handle DELETE requests to post reaction"""
    post_reaction = PostReaction.objects.get(pk=pk)
    post_reaction.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
