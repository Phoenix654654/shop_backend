from django.db import models


class UserRoleEnum(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    SELLER = 'seller', 'Seller'
    BUYER = 'buyer', 'Buyer'
