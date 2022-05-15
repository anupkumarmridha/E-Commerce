# Generated by Django 4.0.2 on 2022-05-14 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_product_total_sell_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField()),
                ('emp_name', models.CharField(max_length=255)),
                ('purpose', models.CharField(choices=[('Personal Use', 'Personal Use'), ('Company Use', 'Company Use')], max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.order')),
            ],
        ),
    ]