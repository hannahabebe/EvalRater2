# Generated by Django 4.2 on 2023-07-31 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0007_remove_task_assigned_to_task_assigned_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('view_manager_pages', 'Can view manager pages'), ('view_employee_pages', 'Can view employee pages')]},
        ),
    ]
