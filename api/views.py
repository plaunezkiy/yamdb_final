from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from titles.models import Title
from .models import Review
from .permissions import IsAdminOrStaff, IsAuthorOrReadOnly, IsModerator
from .serializers import CommentsSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly &
                          (IsAuthorOrReadOnly | IsModerator | IsAdminOrStaff)]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return self.queryset.filter(title=title)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=request.user, title=title)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly &
                          (IsAuthorOrReadOnly | IsModerator | IsAdminOrStaff)]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=title)
        queryset = review.comments.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title)

        serializer.save(author=request.user, review=review)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
