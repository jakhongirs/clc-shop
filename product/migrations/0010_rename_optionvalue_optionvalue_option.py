# Generated by Django 4.0.6 on 2022-07-27 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='optionvalue',
            old_name='optionValue',
            new_name='option',
        ),
    ]
