# Generated by Django 5.1.1 on 2024-12-15 07:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_fooditem_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'food_item')},
        ),
    ]