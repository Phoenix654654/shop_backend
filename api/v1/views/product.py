from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.v1.filters.product import CategoryFilter, ProductFilter
from api.v1.serializers.product import CategoryCreateSerializer, CategoryListSerializer, CategoryRetrieveSerializer, \
    ProductCreateSerializer, ProductListSerializer, ProductUpdateSerializer, ProductRetrieveSerializer, \
    CategoryUploadImageSerializer, ProductImagesCreateSerializer
from apps.common.helpers.helpers import process_and_resize_image
from apps.common.helpers.pagination import CustomPagination
from apps.product.models import Category, Product, ProductVariant, ProductImage


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filterset_class = CategoryFilter

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return (IsAdminUser(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        elif self.action == "retrieve":
            return CategoryRetrieveSerializer
        return self.serializer_class


class ProductViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return (IsAdminUser(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "update":
            return ProductUpdateSerializer
        elif self.action == "retrieve":
            return ProductRetrieveSerializer
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data
        details = serializer_data.pop("details", [])
        product = Product.objects.create(**serializer_data)
        product_variants = [
            ProductVariant(product=product, **data)
            for data in details
        ]
        ProductVariant.objects.bulk_create(product_variants)

        return Response(ProductRetrieveSerializer(product).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        details = serializer_data.pop("details", [])

        for attr, value in serializer_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_ids = [data.get("id").id for data in details if data.get("id")]
        ProductVariant.objects.filter(product=instance).exclude(id__in=existing_ids).delete()
        for party_data in details:
            if "id" in party_data:
                party = ProductVariant.objects.get(id=party_data.pop("id").id)
                for attr, value in party_data.items():
                    setattr(party, attr, value)
                party.save()
            else:
                ProductVariant.objects.create(product=instance, **party_data)
        return Response(ProductRetrieveSerializer(instance).data, status=status.HTTP_200_OK)


class CategoryUploadImageViewSet(APIView):
    serializer_class = CategoryUploadImageSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        image = serializer_data.get("image")

        category, created = Category.objects.update_or_create(
            id=kwargs.get("pk"), defaults={"image": image}
        )

        image_file, filename = process_and_resize_image(category.image.path, (120, 120))
        category.resized_image.save(f"resized_{filename}", image_file)

        return Response({"message": "success"}, status=status.HTTP_201_CREATED)


class ProductUploadImagesViewSet(APIView):
    serializer_class = ProductImagesCreateSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        images_data = serializer.validated_data.pop("images", [])
        output_data = []
        for image in images_data:
            item = ProductImage.objects.create(product_id=kwargs["pk"], image=image)
            output_data.append({
                "id": item.id,
                "product": item.product_id,
                "image": item.image.url,
                "resized_image": item.resized_image.url
            })
        return Response(output_data, status=status.HTTP_201_CREATED)


class ProductDeleteImagesViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def destroy(self, request, pk):
        images = ProductImage.objects.filter(product_id=pk)
        images.delete()
        return Response(
            {"message": "success"}, status=status.HTTP_204_NO_CONTENT,
        )


class ProductDeleteImageViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def destroy(self, request, image_id):
        image = get_object_or_404(ProductImage, id=image_id)
        image.delete()
        return Response(
            {"message": "success"}, status=status.HTTP_204_NO_CONTENT,
        )
