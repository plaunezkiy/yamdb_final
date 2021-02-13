from django.db.models import Avg
from rest_framework import serializers
from .models import Title
from categories.serializers import CategorySerializer, Category
from genres.serializers import GenreSerializer, Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
        return rating or None

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'
