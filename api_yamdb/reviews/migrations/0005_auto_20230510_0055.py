# Generated by Django 3.2 on 2023-05-10 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230509_1459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_query_name='titles', to='reviews.category', verbose_name='Категория'),
        ),
    ]
