from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscribe, User
from recipes.pagination import CustomPagination
from .serializers import FollowListSerializer, SubscribeSerializer


class FollowViewSet(UserViewSet):
    """ViewSet подписок на авторов."""
    queryset = User.objects.all()
    serializer_class = FollowListSerializer
    pagination_class = CustomPagination

    @action(detail=True,
            methods=['POST'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        """Подписка на автора."""
        data = {'user': request.user.id, 'author': id}
        serializer = SubscribeSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        """Отписка от автора."""
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(Subscribe, user=user, author=author)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        """Просмотр подписок."""
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
