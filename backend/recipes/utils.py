from django.http import HttpResponse


def make_shopping_list(ingredients):
    shopping_cart = '\n'.join([
        f'{ingredient["ingredient__name"]}: {ingredient["number"]}'
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients
    ])
    response = HttpResponse(shopping_cart, content_type='text')
    response['Content-Disposition'] = (
        'attachment;filename=shopping_cart.pdf')
    return response


def representation(context, instance, serializer):
    request = context.get('request')
    new_context = {'request': request}
    return serializer(instance, context=new_context).data
