import django_filters as filters

from titles.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug', method='filter_genre')
    category = filters.CharFilter(field_name='category__slug', method='filter_category')
    year = filters.NumberFilter(field_name='year', method='filter_year')
    name = filters.CharFilter(field_name='name', method='filter_name')

    class Meta:
        model = Title
        fields = ('genre', 'category')

    def filter_genre(self, queryset, name, tags):
        return queryset.filter(genre__slug=tags)

    def filter_category(self, queryset, name, tags):
        return queryset.filter(category__slug=tags)

    def filter_year(self, queryset, name, tags):
        return queryset.filter(year=tags)

    def filter_name(self, queryset, name, tags):
        return queryset.filter(name__icontains=tags)
