# Generated by Django 5.2.1 on 2025-05-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_withdrawal_wallet_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
