# products/admin.py
from django.contrib import admin
from .models import Product, Vote, Comment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'status', 'user', 'created_at')  # Fields to display in admin list view
    list_filter = ('status', 'available_countries')  # Filters in the sidebar
    search_fields = ('title', 'brand', 'available_countries', 'ingredients')  # Searchable fields
    actions = ['approve_product', 'reject_product']  # Actions for approving/rejecting products

    # Action to approve selected products
    def approve_product(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected products have been approved.")
    approve_product.short_description = "Approve selected products"

    # Action to reject selected products
    def reject_product(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected products have been rejected.")
    reject_product.short_description = "Reject selected products"

admin.site.register(Product, ProductAdmin)
admin.site.register(Vote)
admin.site.register(Comment)


######################## Ingredntis ###############################

# admin.py
from django.contrib import admin
from .models import Ingredient, IngredientComment

# Register the Ingredient model
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'votes_halal', 'votes_haram')
    search_fields = ('name',)
    list_filter = ('status',)

# Register IngredientComment model for managing comments
@admin.register(IngredientComment)
class IngredientCommentAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'user', 'created_at')
    search_fields = ('ingredient__name', 'user__username')
