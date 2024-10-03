# products/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product,Ingredient, IngredientComment
from .serializers import ProductSerializer,IngredientSerializer, IngredientCommentSerializer
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(status='pending', user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='approve')
    def approve_product(self, request, pk=None):
        product = self.get_object()
        if request.user.is_admin:
            product.status = 'approved'
            product.save()
            return Response({'status': 'approved'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='reject')
    def reject_product(self, request, pk=None):
        product = self.get_object()
        if request.user.is_staff:
            product.status = 'rejected'
            product.save()
            return Response({'status': 'rejected'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    


########################### ForInredeitnts ###################################

 # views.py


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    @action(detail=True, methods=['post'], url_path='vote-halal')
    def vote_halal(self, request, pk=None):
        ingredient = self.get_object()
        # Add logic for voting halal (e.g., increment a vote count, etc.)
        return Response({'message': 'Voted as halal'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='vote-haram')
    def vote_haram(self, request, pk=None):
        ingredient = self.get_object()
        # Add logic for voting haram (e.g., increment a vote count, etc.)
        return Response({'message': 'Voted as haram'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        ingredient = self.get_object()
        comments = ingredient.comments.all()
        serializer = IngredientCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='add-comment')
    def add_comment(self, request, pk=None):
        ingredient = self.get_object()
        comment = IngredientComment.objects.create(
            ingredient=ingredient,
            user=request.user,
            content=request.data['content']
        )
        return Response({'status': 'Comment added'}, status=status.HTTP_201_CREATED)
    
 ###################### Search Functinality ###################
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
   
    
