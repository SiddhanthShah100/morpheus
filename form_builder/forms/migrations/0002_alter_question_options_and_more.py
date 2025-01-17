# Generated by Django 5.1.4 on 2025-01-05 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='option',
            old_name='text',
            new_name='option_text',
        ),
        migrations.AddField(
            model_name='question',
            name='matrix_columns',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='matrix_rows',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_choices', to='forms.question'),
        ),
    ]
