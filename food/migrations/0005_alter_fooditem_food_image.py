# Generated by Django 5.1.1 on 2024-11-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_alter_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_image',
            field=models.ImageField(blank=True, default='', upload_to='image/'),
        ),
    ]
