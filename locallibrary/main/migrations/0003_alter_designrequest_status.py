# Generated by Django 3.2.25 on 2024-11-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_designrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designrequest',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('in_progress', 'Принято в работу'), ('completed', 'Выполнено')], default='new', max_length=20),
        ),
    ]
