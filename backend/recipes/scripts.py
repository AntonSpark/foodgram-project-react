import json
from .models import Ingredient


def fill_database():
    # delete 
    Ingredient.objects.all().delete()
    
    # python run.py recipes.scripts "fill_database()"
    print(Ingredient.objects.all())
    
    ingredients_list = json.load("../static/data/ingredients.json")
    print(ingredients_list)
    #Решить здачу в две строчки:
    for d in ingredients_list:
        ingridient = Ingredient()
        ingridient.name = d["name"]
        ingridient.measurement_unit = d["measurement_unit"]
        ingridient.save()
    
    print(ingredients_list)
    #Мы должны заполнить модель Recipe.
    
    
    """
    сделать тестовое наполнение базы скриптом
    создать репозиторий на гитхабе
    и запушить это творение туда.
    """
