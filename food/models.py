import os
from tabnanny import verbose
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from account.models import UserProfile ,User
from os.path import basename
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden
from django.db.models import Count 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()
        existing_categories = Category.objects.filter(category_name=self.category_name)
        if self.pk:
            existing_categories = existing_categories.exclude(pk=self.pk)
        if existing_categories.exists():
            raise ValidationError(f"{self.category_name} already exists as a category.")

    def __str__(self):
        return self.category_name

    def num_projects(self):
        return self.project_set.count()





class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': User.ADMIN } ) # Limit choices to vendor users
    food_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=100, unique=True , null=True , blank=True)
    
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    

    food_image = models.ImageField(upload_to='image/', default='', blank=True)

    is_available = models.BooleanField(default=True)
    is_soldout=models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'FoodItem'
        verbose_name_plural = 'FoodItems'

    def __str__(self):
        return self.food_name
    
    def save(self, *args, **kwargs):
        self.food_name = self.food_name.title()  # Ensure the food name is capitalized

        if not self.slug:
            # Generate the slug if it's empty
            self.slug = slugify(self.food_name)
            # Ensure the slug is unique
            if FoodItem.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        super(FoodItem, self).save(*args, **kwargs)




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'food_item') 

    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type



class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who gives the rating
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  # Food item being rated
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),  # Minimum rating is 1.0
            MaxValueValidator(5.0)  # Maximum rating is 5.0
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the rating is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates to the rating

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = ('user', 'food_item')  
    def __str__(self):
        return f"{self.user} - {self.food_item} - {self.rating}"
