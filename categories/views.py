from rest_framework import viewsets, status, filters
from rest_framework.response import Response

from api.permissions import IsAdminOrStaff, ReadOnly
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminOrStaff]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)
    http_method_names = ["get", "post", "delete"]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
