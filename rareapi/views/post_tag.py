from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import PostTag, Tag, Post
from rareapi.views import TagSerializer


class PostTagView(ViewSet):
  """Post tag view"""
  
  def retrieve(self, request, pk):
    try:
      post_tag = PostTag.objects.get(pk=pk)
      serializer = PostTagSerializer(post_tag)
      return Response(serializer.data)
    except PostTag.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  # def list(self, request):
    # post_tags = PostTag.objects.all()
    # post = request.query_params.get('post', None)
    # if post is not None:
    #   post_tags = post_tags.filter(post_id=post)
      
    # serializer = PostTagSerializer(post_tags, many=True)
    # return Response(serializer.data)

    
  def list(self, request):
    def get_tags_for_post(post_id):
      post = Post.objects.get(id=post_id)
      post_tags = PostTag.objects.filter(post=post)
      tags = []
      for post_tag in post_tags:
        tags.append(post_tag.tag)
      return tags
        
    post_id = request.query_params.get('post', None)
    if post_id is not None:
      tags = get_tags_for_post(post_id)
      serializer = TagSerializer(tags, many=True)
      return Response(serializer.data)
    else:
      post_tags = PostTag.objects.all()
      serializer = PostTagSerializer(post_tags, many=True)
      return Response(serializer.data)
  
  def create(self, request):
    tag = Tag.objects.get(id=request.data["tag_id"])
    post = Post.objects.get(pk=request.data["post_id"])
    
    post_tag = PostTag.objects.create(
      post=post,
      tag=tag
    )
    serializer = PostTagSerializer(post_tag)
    return Response(serializer.data)
  
  def update(self, request, pk):
    post_tag = PostTag.objects.get(pk=pk)
    post_tag.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    post_tag = PostTag.objects.get(pk=pk)
    post_tag.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class PostTagSerializer(serializers.ModelSerializer):
  """serializer for post tags"""
  
  class Meta:
    model = PostTag
    depth = 1
    fields = ('id', 'post_id', 'tag_id')
    depth = 1
