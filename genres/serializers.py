from rest_framework import serializers
from rest_framework import validators
from .models import Genre


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField(validators=[validators.UniqueValidator(queryset=Genre.objects.all())])

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre
