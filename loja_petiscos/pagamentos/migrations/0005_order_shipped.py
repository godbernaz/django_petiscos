# Generated by Django 5.1.2 on 2024-12-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamentos', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]