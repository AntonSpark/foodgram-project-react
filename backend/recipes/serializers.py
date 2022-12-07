from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField, ValidationError)
from drf_base64.fields import Base64ImageField

from users.serializers import CustomUserSerializer
from .models import (
    FavoriteRecipe, Ingredient, AmountIngredient, Recipe, ShoppingCart, Tag
)


class TagSerializer(ModelSerializer):
    """Сериализатор тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(ModelSerializer):
    """Сериализатор количества ингредиентов в рецепте."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(ModelSerializer):
    """Сериализатор рецепта."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountIngredientSerializer(
        many=True, source='ingredient_for_recipe'
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_object_exists(self, model, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and model.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        )

    def get_is_favorited(self, obj):
        return self.get_is_object_exists(FavoriteRecipe, obj)

    def get_is_in_shopping_cart(self, obj):
        return self.get_is_object_exists(ShoppingCart, obj)


class AmountIngredientForRecipeCreatSerializer(serializers.ModelSerializer):
    """Сериализатор наполнения рецепта ингредиентами."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class RecipeCreatSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True
    )
    ingredients = AmountIngredientForRecipeCreatSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'image', 'tags', 'ingredients',
            'text', 'cooking_time', 'id'
        )

    def validate(self, data):
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError('Добавьте ингредиент')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться'
                )
            ingredients_list.append(ingredient_id)
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError('Добавьте тэг')
        return data

    def add_ingredients_and_tags(self, recipe, ingredients, tags):
        objects = [
            AmountIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ]
        AmountIngredient.objects.bulk_create(objects)
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients_and_tags(recipe, ingredients, tags)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        AmountIngredient.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.add_ingredients_and_tags(recipe, ingredients, tags)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        serializer = RecipeListSerializer(instance)
        return serializer.data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор содержания рецепта."""
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов"""
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = data['recipe']
        if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError('Рецепт добавлен в избранное!')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта в корзину"""
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = data['recipe']
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Рецепт уже в корзине!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance.recipe, context=context).data
