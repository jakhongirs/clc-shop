# Generated by Django 4.0.6 on 2022-07-27 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_option_slug_optionvalue_slug_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='product_image'),
        ),
    ]