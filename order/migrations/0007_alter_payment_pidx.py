# Generated by Django 5.1.1 on 2024-12-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_foodorder_reservation_expiration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pidx',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
