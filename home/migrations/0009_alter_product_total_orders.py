# Generated by Django 4.0.2 on 2022-05-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_product_order_status_product_total_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='total_orders',
            field=models.IntegerField(default=0),
        ),
    ]
