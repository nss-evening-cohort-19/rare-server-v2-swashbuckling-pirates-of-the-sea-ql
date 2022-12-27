from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, User, Category, PostReaction, Reaction
# from rareapi.views import ReactionSerializer

class PostView(ViewSet):
  """View set for post requests"""
  def retrieve(self, request, pk):
    """Handle GET requests for a single post"""
    try:
      post = Post.objects.get(id=pk)
      
      post_reactions = PostReaction.objects.filter(post=post.id)
      reactions_on_posts = []
      
      for reaction_obj in post_reactions:
        try:
          reactions_on_post = Reaction.objects.get(id=reaction_obj.reaction_id)
          reactions_on_posts_dict = {}
          reactions_on_posts_dict['id'] = reactions_on_post.id
          reactions_on_posts_dict['label'] = reactions_on_post.label
          reactions_on_posts_dict['image_url'] = reactions_on_post.image_url
          reactions_on_posts.append(reactions_on_posts_dict)
        except:
          pass

      post.reactions_on_posts = reactions_on_posts
      
      serializer = PostSerializer(post)
      return Response(serializer.data)
    except Post.DoesNotExist as e:
      return Response({'message': e.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests for all posts"""
    posts = Post.objects.all()
    
    post_category = request.query_params.get('category', None)
    if post_category is not None:
      posts = posts.filter(category_id=post_category)
      
    post_user = request.query_params.get('user', None)
    if post_user is not None:
      posts = posts.filter(user_id=post_user)
      
    for post in posts:
      post_reactions = PostReaction.objects.filter(post=post.id)
      reactions_on_posts = []
      
      for post_reaction_obj in post_reactions:
        try:
          reactions_on_post = Reaction.objects.get(id=post_reaction_obj.reaction_id)
          reactions_on_posts_dict = {}
          reactions_on_posts_dict['id'] = reactions_on_post.id
          reactions_on_posts_dict['label'] = reactions_on_post.label
          reactions_on_posts_dict['image_url'] = reactions_on_post.image_url
          reactions_on_posts.append(reactions_on_posts_dict)
        except:
          pass
        post.reactions_on_posts = reactions_on_posts
      
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
  
    
  def create(self, request):
    """Handle POST requests for a single post"""
    user = User.objects.get(id=request.data["user_id"])
    category = Category.objects.get(id=request.data["category_id"])
    post = Post.objects.create(
      title = request.data["title"],
      publication_date = request.data["publication_date"],
      image_url = request.data["image_url"],
      content = request.data["content"],
      user_id = user,
      category_id =category
      )
    serializer = PostSerializer(post)
    return Response(serializer.data)
  
  def update(self, request, pk):
    "Handle PUT requests for a single post"""
    post = Post.objects.get(pk=pk)
    post.user_id = User.objects.get(id=request.data["user_id"])
    post.category_id = Category.objects.get(id=request.data["category_id"])
    post.title = request.data["title"]
    post.publication_date = request.data["publication_date"]
    post.image_url = request.data["image_url"]
    post.content = request.data["content"]
    post.save()
    
    serializer = PostSerializer(post)
    return Response(serializer.data)
  
  def delete(self, request, pk):
    """Handle DELETE requests for a single post"""
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
   
  
class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'reactions_on_posts')
    depth = 1
