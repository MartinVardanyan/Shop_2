# Generated by Django 3.0.4 on 2020-05-20 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20200511_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Administrator'),
        ),
        migrations.AddField(
            model_name='item',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Customer'),
        ),
    ]
