from django_filters import CharFilter, FilterSet

from .models import Title


class TitleFilter(FilterSet):
    """Filter title on genre, category and name"""
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']
