# Create your models here.
import os
from django.db import models
from api.utils import save_pet_image


class User(models.Model):
    AREA_CHOICES = (
        ("desarrollo", "Desarrollo"),
        ("diseno", "Diseño"),
        ("ventas", "Ventas"),
    )
    area = models.CharField(max_length=10, choices=AREA_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_user_by_email(email: str):
        try:
            return User.objects.get(email=email)
        except:
            return None


class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=save_pet_image, null=True, blank=True)
    short_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    def get_pets_by_user(user: User):
        try:
            return Pet.objects.filter(user=user)
        except:
            return []


class Toy(models.Model):
    pets = models.ManyToManyField(Pet, related_name="toys")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_url = models.URLField()

    def __str__(self):
        return f"{self.name}"
