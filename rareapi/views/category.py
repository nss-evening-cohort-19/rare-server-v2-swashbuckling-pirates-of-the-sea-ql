from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CatView(ViewSet):
    """Category view"""
    def retrieve(self, request, pk):
        """Handle GET request for single category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CatSerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET request for all categories
        """
        categories = Category.objects.all()
        serializer = CatSerializer(categories, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """"""
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        category = Category.objects.create(
            label=request.data["label"]
        )
        serializer = CatSerializer(category)
        return Response(serializer.data)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1