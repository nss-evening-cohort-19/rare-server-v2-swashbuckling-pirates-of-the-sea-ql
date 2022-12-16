"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import User

class UserView(ViewSet):
  """Rare User View"""
  
  def retrieve(self, request, pk):
    """Handle GET single user"""
    try:
      user = User.objects.get(pk=pk)
      serializer = UserSerializer(user)
      return Response(serializer.data)
    
    except User.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get users by uid"""
    users = User.objects.all()
    
    uid = request.META['HTTP_AUTHORIZATION']
    if uid is not None:
      users = users.filter(uid=uid)
      
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
class UserSerializer(serializers.ModelSerializer):
  """JSON serializer for Users"""
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'bio', 'profile_image_url', 'email', 'created_on', 'active')
      