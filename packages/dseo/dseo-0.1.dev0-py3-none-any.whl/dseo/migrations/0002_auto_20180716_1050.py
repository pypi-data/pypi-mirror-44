# Generated by Django 2.0.7 on 2018-07-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dseo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metadata',
            options={'verbose_name': 'Мета дані', 'verbose_name_plural': 'Мета дані'},
        ),
        migrations.AlterField(
            model_name='counter',
            name='code',
            field=models.TextField(default=None, max_length=5000, verbose_name='Дані'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='keywords',
            field=models.CharField(blank=True, max_length=255, verbose_name='Ключові слова'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='robots',
            field=models.CharField(blank=True, choices=[('', '---------'), ('index, follow', 'index, follow'), ('index, nofollow', 'index, nofollow'), ('noindex, nofollow', 'noindex, nofollow'), ('noindex, follow', 'noindex, follow')], max_length=20, verbose_name='Індексувати та переходити за посиланнями?'),
        ),
    ]
