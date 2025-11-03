from rest_framework import serializers

from apps.product.models import Category, Product, ProductImage, ProductVariant


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id", "name_ru", "name_kg", "name_en", "left_ordering", "right_ordering"
        )


class CategoryListSerializer(serializers.ModelSerializer):
    price_from = serializers.SerializerMethodField(method_name="get_minimum_price")

    def get_minimum_price(self, instance):
        products = Product.objects.filter(category=instance)
        minimum_price = ProductVariant.objects.filter(product__in=products).order_by("price").first()
        return minimum_price.price if minimum_price else None

    class Meta:
        model = Category
        fields = (
            "id", "name_ru", "name_kg", "name_en", "left_ordering", "right_ordering", "image", "resized_image",
            "price_from"
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id", "image", "resized_image"
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            "id", "product", "color", "size", "quantity", "price", "discount_price"
        )


class ProductInCategorySerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    details = ProductVariantSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            "id", "name_ru", "name_kg", "name_en", "description", "category",
            "recommended", "bestsellers", "promotional", "characteristics", "code_name", "images", "details"
        )


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    products = ProductInCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id", "name_ru", "name_kg", "name_en", "left_ordering", "right_ordering", "image", "resized_image",
            "products"
        )


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id", "product", "image", "resized_image"
        )


class CategoryUploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ProductImagesCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            "id", "color", "size", "quantity", "price", "discount_price"
        )


class ProductVariantUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ProductVariant.objects.all(),
                                            required=False)

    class Meta:
        model = ProductVariant
        fields = (
            "id", "color", "size", "quantity", "price", "discount_price"
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    details = ProductVariantCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name_ru", "name_kg", "name_en", "description", "category",
            "recommended", "bestsellers", "recommended_left_side", "promotional",
            "characteristics", "code_name", "details"
        )


class ProductUpdateSerializer(serializers.ModelSerializer):
    details = ProductVariantUpdateSerializer(many=True, write_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name_ru", "name_kg", "name_en", "description", "category",
            "recommended", "bestsellers", "recommended_left_side", "promotional",
            "characteristics", "code_name", "details"
        )


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryCreateSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)
    details = ProductVariantSerializer(read_only=True, many=True)
    price_from = serializers.SerializerMethodField(method_name="get_minimum_price")

    def get_minimum_price(self, instance):
        minimum_price = ProductVariant.objects.filter(product=instance).order_by("price").first()
        return minimum_price.price if minimum_price else None

    class Meta:
        model = Product
        fields = (
            "id", "name_ru", "name_kg", "name_en", "description", "category",
            "recommended", "bestsellers", "promotional", "characteristics", "code_name", "images",
            "details", "price_from"
        )


class ProductRetrieveSerializer(serializers.ModelSerializer):
    category = CategoryCreateSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)
    details = ProductVariantSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            "id", "name_ru", "name_kg", "name_en", "description", "category",
            "recommended", "bestsellers", "promotional", "characteristics", "code_name", "images", "details"
        )
