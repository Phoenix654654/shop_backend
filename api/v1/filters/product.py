import django_filters
from django.db.models import When, Value, Case, IntegerField, Q

from apps.product.models import Category, Product


class CategoryFilter(django_filters.FilterSet):
    left_ordering = django_filters.BooleanFilter(method='by_ordering', field_name='left_ordering')
    right_ordering = django_filters.BooleanFilter(method='by_ordering', field_name='right_ordering')

    def by_ordering(self, queryset, name, value):
        if value:
            return queryset.annotate(
                is_null=Case(
                    When(**{f'{name}__isnull': True}, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('is_null', name)
        else:
            return queryset.annotate(
                is_null=Case(
                    When(**{f'{name}__isnull': True}, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('is_null', f'-{name}')

    class Meta:
        model = Category
        fields = ('id', 'left_ordering', 'right_ordering')


class ProductFilter(django_filters.FilterSet):
    product_ids = django_filters.CharFilter(method='filter_by_product_ids')
    search_by = django_filters.CharFilter(method='search')

    class Meta:
        model = Product
        fields = (
            "recommended", "recommended_left_side", "bestsellers", "promotional", "category", "product_ids", "search_by"
        )

    def filter_by_product_ids(self, queryset, name, value):
        if value:
            if value.lower() == 'false':
                return queryset.none()
            product_ids = value.split(',')
            queryset = queryset.filter(id__in=product_ids)
        return queryset

    def search(self, queryset, *args, **kwargs):
        return queryset.filter(
            Q(name_ru__icontains=args[1]) |
            Q(name_kg__icontains=args[1]) |
            Q(name_en__icontains=args[1]) |
            Q(code_name__icontains=args[1])
        )
