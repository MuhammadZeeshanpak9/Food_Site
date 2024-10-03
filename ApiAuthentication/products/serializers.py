# products/serializers.py
from rest_framework import serializers
from .models import Product,Ingredient, IngredientComment
 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'available_countries', 'description', 'barcode', 'brand', 'ingredients']


###########################INNGREDEINTS######################################

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'status', 'votes_halal', 'votes_haram']

class IngredientCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientComment
        fields = ['id', 'ingredient', 'user', 'content', 'created_at']




