from rest_framework import serializers
from rest_framework import validators
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField(
        validators=[
            validators.UniqueValidator(queryset=Category.objects.all())
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Category
