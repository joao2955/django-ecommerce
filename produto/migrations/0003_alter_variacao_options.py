# Generated by Django 5.0 on 2023-12-20 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_variacao_estoque_alter_variacao_preco_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variacao',
            options={'verbose_name': 'Variação', 'verbose_name_plural': 'Variações'},
        ),
    ]