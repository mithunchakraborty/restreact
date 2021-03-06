# Generated by Django 3.1 on 2020-08-31 18:41

from django.db import migrations


def create_data(apps, schema_editor):
    Customer = apps.get_model('customers', 'Customer')
    Customer(
        first_name='Customer 001',
        last_name='Last name of Customer 001',
        email='customer@gmail.com',
        phone='79130343394',
        address='Address of Customer 001',
        description='Description of Customer 001',
    ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
