# Generated by Django 4.2.16 on 2025-03-07 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement_app', '0005_remove_broadcast_category_broadcast_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='goal',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_details',
            name='how_did_you_learn_about_us',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_details',
            name='type_of_challange',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
