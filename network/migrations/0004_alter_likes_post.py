# Generated by Django 4.0.1 on 2022-02-09 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_following_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='post_id', to='network.posts'),
        ),
    ]
