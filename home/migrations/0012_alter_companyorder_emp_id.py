# Generated by Django 4.0.2 on 2022-05-14 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_companyorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyorder',
            name='emp_id',
            field=models.CharField(max_length=255),
        ),
    ]
