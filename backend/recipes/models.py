from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )

    measurement_unit = models.CharField(
        max_length=120,
        verbose_name='Еденица измерения',
        help_text='Введите еденицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    """Модель тэга."""
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Название тэга',
        help_text='Введите название тэга'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='HEX-код цвета',
        unique=True,
        help_text='Введите цветовой HEX-код без #, например 49B64E'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes_ingredients',
        help_text='Выберите ингредиенты',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Выберите тэги',
        related_name='recipes_tag',
    )

    image = models.ImageField(
        upload_to='recipes/photo/',
        verbose_name='Фото',
        help_text='Фото блюда'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )

    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание рецепта'
    )

    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время готовки в минутах',
        help_text='Введите время готовки в минутах',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """Модель количества ингредиентов для рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_for_recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_for_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Введите количество ингредиента для рецепта'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_for_recipe'
            )
        ]

    def __str__(self):
        return f'Количество{self.ingredient} в {self.recipe}:{self.amount}'


class FavoriteRecipe(models.Model):
    """Модель рецептов добавленный в корзину."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном пользователя {self.user}'


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Пользователь',
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_shopping_cart',
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
