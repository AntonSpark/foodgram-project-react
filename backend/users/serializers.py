from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from .models import Subscribe, User

RECIPES_LIMIT = 3


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации создания пользователя."""
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'password'
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Subscribe.objects.filter(user=user, author=obj).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода авторов на которых подписан пользователь."""
    class Meta:
        model = Subscribe
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=['user', 'author']
            )
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя'
            )
        return data

    def to_representation(self, instance):
        return FollowListSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта в избранное."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка подписок.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        """Проверяет подписан ли текущий пользователь на автора."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Subscribe.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:RECIPES_LIMIT]
        return FavoriteRecipesSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        """Показывает количество рецептов у автора."""
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()
