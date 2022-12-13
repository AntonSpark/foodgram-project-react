from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (
    FavoriteRecipe, Ingredient, AmountIngredient, Recipe, ShoppingCart, Tag
)
from .pagination import CustomPagination
from .permissions import IsAllowedOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeListSerializer,
    RecipeCreatSerializer, ShoppingCartSerializer, TagSerializer
)
from .utils import make_shopping_list


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAllowedOrReadOnly,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeCreatSerializer
    
    def get_error(self):
        if self.request.method.GET and self.request.method.GET["error"]:
            print ('ddd')

    @staticmethod
    def create_object(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_object(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        object = get_object_or_404(model, user=user, recipe=recipe)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create_or_delete(self, http_method, recipe, key, model, serializer):
        if http_method == 'POST':
            return self.create_object(request=recipe, pk=key,
                                      serializers=serializer)
        return self.delete_object(request=recipe, pk=key, model=model)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def in_favorite(self, request, pk):
        return self.create_or_delete(
            request.method, request, pk, FavoriteRecipe, FavoriteSerializer
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def in_shopping_cart(self, request, pk):
        return self.create_or_delete(
            request.method, request, pk, ShoppingCart, ShoppingCartSerializer
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes = AmountIngredient.objects.filter(
            recipe__shopping_cart__user=user
        )
        ingredients = recipes.values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(number=Sum('amount'))

        return make_shopping_list(ingredients)
