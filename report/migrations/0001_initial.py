# Generated by Django 5.1.2 on 2024-11-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('transaction_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('quantity_sold', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('date_sold', models.DateField()),
                ('customer_id', models.IntegerField()),
            ],
        ),
    ]