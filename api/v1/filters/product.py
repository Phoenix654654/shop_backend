import django_filters
from django.db.models import When, Value, Case, IntegerField, Q

from apps.product.models import Category, Product


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
