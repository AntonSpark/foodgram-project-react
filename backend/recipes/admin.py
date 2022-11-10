from django.contrib import admin

from .models import (
    Ingredient, Tag, Recipe, AmountIngredient,
    FavoriteRecipe, ShoppingCart
)


EMPTY_VALUE = '-пусто-'


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE



@admin.register(AmountIngredient)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient','recipe', 'amount')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY_VALUE


class AmountIngredientsInline(admin.TabularInline):
    model =AmountIngredient
    min_num = 1


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'image',
        'text', 'cooking_time', 'favorite_count',
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = EMPTY_VALUE
    inlines = (AmountIngredientsInline,)

    def favorite_count(self, recipe):
        """Количество добавлений в избранное."""
        return recipe.favorite.count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE