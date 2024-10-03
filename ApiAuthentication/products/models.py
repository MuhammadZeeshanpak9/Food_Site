# products/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

class Product(models.Model):
    title = models.CharField(max_length=255)
    available_countries = models.CharField(max_length=255)
    description = models.TextField()
    barcode = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255)
    ingredients = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
# Updated to use custom user model
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field is added
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use custom user model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    product = models.ForeignKey(Product, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use custom user model
    vote_type = models.CharField(max_length=10, choices=[('halal', 'Halal'), ('haram', 'Haram')])
    created_at = models.DateTimeField(auto_now_add=True)

###########################INGREDEINTS##################################

class Ingredient(models.Model):
    HALAL_HARAM_CHOICES = [
        ('halal', 'Halal'),
        ('haram', 'Haram')
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=5, choices=HALAL_HARAM_CHOICES, default='halal')
    votes_halal = models.IntegerField(default=0)
    votes_haram = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class IngredientComment(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ingredient.name}"