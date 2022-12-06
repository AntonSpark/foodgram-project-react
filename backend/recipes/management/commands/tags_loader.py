from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#ffc000', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#2286e0', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#6c52ba', 'slug': 'supper'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Тэги в базе!'))
