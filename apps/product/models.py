from django.db import models

from apps.common.helpers.helpers import process_and_resize_image


class Category(models.Model):
    """Категория товара"""
    name_ru = models.CharField(max_length=128)
    name_kg = models.CharField(max_length=128, null=True)
    name_en = models.CharField(max_length=128, null=True)
    image = models.ImageField(upload_to='category/original_images/', blank=True, null=True)
    resized_image = models.ImageField(upload_to='category/resized_images/', blank=True, null=True)

    class Meta:
        db_table = "category"
        ordering = ["-id"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Товар"""
    name_ru = models.CharField(max_length=128)
    name_kg = models.CharField(max_length=128, null=True)
    name_en = models.CharField(max_length=128, null=True)
    description = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    recommended = models.BooleanField(default=False)
    recommended_left_side = models.BooleanField(default=False)
    bestsellers = models.BooleanField(default=False)
    promotional = models.BooleanField(default=False)
    characteristics = models.JSONField(null=True)
    code_name = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = "product"
        ordering = ["-id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/original_images/')
    resized_image = models.ImageField(upload_to='products/resized_images/', blank=True, null=True)

    class Meta:
        db_table = "product_image"
        ordering = ["-id"]
        verbose_name = "Изображения товара"
        verbose_name_plural = "Изображения товаров"

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        image_file, filename = process_and_resize_image(self.image.path, (80, 80))
        self.resized_image.save(f"resized_{filename}", image_file, save=False)
        super(ProductImage, self).save(update_fields=['resized_image'])


class ProductVariant(models.Model):
    """Детали продукта"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="details")
    color = models.JSONField()
    size = models.CharField(max_length=32)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        db_table = "product_variant"
        ordering = ["-id"]
        verbose_name = "Детали продукта"
        verbose_name_plural = "Детали продуктов"


