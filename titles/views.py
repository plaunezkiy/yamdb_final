from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from api.permissions import ReadOnly, IsAdminOrStaff
from .filters import TitleFilter
from .models import Title
from .serializers import TitlePostSerializer, TitleGetSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [ReadOnly | IsAdminOrStaff]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleGetSerializer
        return TitlePostSerializer
