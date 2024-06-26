# Generated by Django 5.0.4 on 2024-04-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_alter_customer_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(default="Cash on Delivery", max_length=100),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Order Received", "Order Received"),
                    ("Order Processing", "Order Processing"),
                    ("Order Shipped", "Order Shipped"),
                    ("Order Delivered", "Order Delivered"),
                    ("Order Cancelled", "Order Cancelled"),
                ],
                default="Order Processing",
                max_length=100,
            ),
        ),
    ]
