# Generated by Django 3.1.6 on 2021-02-24 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('order', '0003_auto_20210223_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='option',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.address'),
        ),
    ]
