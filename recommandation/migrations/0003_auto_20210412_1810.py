# Generated by Django 3.1.7 on 2021-04-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommandation', '0002_auto_20210411_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='season',
            field=models.CharField(max_length=200),
        ),
    ]