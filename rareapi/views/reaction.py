from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction

class ReactionSerializer(serializers.ModelSerializer):
  class Meta:
      model = Reaction
      fields = ('id', 'label', 'image_url')
      depth = 1

class ReactionView(ViewSet):
  """ ViewSet for Reaction Requests"""
  def list(self, request):
    """Handle GET requests for Reactions"""
    reactions = Reaction.objects.all()
    
    serializer = ReactionSerializer(reactions, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    """Handle Requests for GET single reaction"""
    try:
      reaction = Reaction.objects.get(pk=pk)
      serializer = ReactionSerializer(reaction)
      return Response(serializer.data)
    except Reaction.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

  def create(self, request):
    """Handle POST requests to reaction"""
    reaction = Reaction.objects.create(
      label = request.data["label"],
      image_url = request.data["image_url"]
    )
    serializer = ReactionSerializer(reaction)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT requests for reaction"""
    reaction = Reaction.objects.get(pk=pk)
    reaction.label = request.data["label"]
    reaction.image_url = request.data["image_url"]
    reaction.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    """Handle DELETE requests to reaction"""
    reaction = Reaction.objects.get(pk=pk)
    reaction.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
