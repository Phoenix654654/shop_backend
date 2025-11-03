from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.views.product import ProductDeleteImagesViewSet, CategoryUploadImageViewSet, ProductUploadImagesViewSet, \
    ProductDeleteImageViewSet, ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register("category", CategoryViewSet)
router.register("product", ProductViewSet)
urlpatterns = [
    path('category/<int:pk>/upload_image/', CategoryUploadImageViewSet.as_view()),
    path('product/<int:pk>/upload_images/', ProductUploadImagesViewSet.as_view()),
    path('product/<int:pk>/delete_images/', ProductDeleteImagesViewSet.as_view({"delete": "destroy"})),
    path('product/<int:image_id>/delete_image/', ProductDeleteImageViewSet.as_view({"delete": "destroy"})),
]
urlpatterns += router.urls
