# Generated by Django 2.2.1 on 2019-06-03 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprofile',
            name='user_have',
            field=models.BooleanField(default=True),
        ),
    ]