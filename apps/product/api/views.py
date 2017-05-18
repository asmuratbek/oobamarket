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
from .pagination import ProductLimitPagination
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from apps.product.models import Product
from .serializers import ProductSerializer, ProductCreateSerializer


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    pagination_class = ProductLimitPagination#PageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        objects = Product.objects.all()

        if self.request.GET.get('search'):
            q = self.request.GET.get('search')
            objects = Product.objects.filter(
                Q(title__icontains=q)|
                Q(text__icontains=q)
            ).distinct()
            return objects
        else:
            objects = Product.objects.all()
            return objects


class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class ProductUpdateApiView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)