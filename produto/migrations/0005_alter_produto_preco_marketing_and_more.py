# Generated by Django 5.0 on 2023-12-23 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(default=0, verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing_promocional',
            field=models.FloatField(default=0, verbose_name='Preço Promo.'),
        ),
        migrations.AlterField(
            model_name='variacao',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variacao',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variacoes_set', to='produto.produto'),
        ),
    ]