# Generated by Django 4.1.3 on 2022-11-18 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='payment_interval',
            field=models.DurationField(help_text='enter in the format: "x days"'),
        ),
    ]