# Generated by Django 4.2 on 2023-07-30 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0005_alter_matrix_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='status',
            field=models.CharField(choices=[('PA', 'Pending Approval'), ('S', 'Scheduled'), ('C', 'Completed'), ('CA', 'Cancelled')], max_length=2, null=True),
        ),
    ]