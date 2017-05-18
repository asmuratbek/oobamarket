from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from .pagination import ShopLimitPagination
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from apps.shop.models import Shop
from .serializers import ShopSerializer, ShopCreateSerializer


class ShopListApiView(ListAPIView):
    serializer_class = ShopSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    pagination_class = ShopLimitPagination#PageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        objects = Shop.objects.all()

        if self.request.GET.get('search'):
            q = self.request.GET.get('search')
            objects = Shop.objects.filter(
                Q(title__icontains=q)|
                Q(text__icontains=q)
            ).distinct()
            return objects
        else:
            objects = Shop.objects.all()
            return objects


class ShopDetailApiView(RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class ShopUpdateApiView(RetrieveUpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ShopDeleteApiView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class ShopCreateApiView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
