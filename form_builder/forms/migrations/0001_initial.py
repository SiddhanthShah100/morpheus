# Generated by Django 5.1.4 on 2025-01-05 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('dropdown', 'Dropdown'), ('checkbox', 'Checkbox'), ('ranking', 'Ranking'), ('linear_scale', 'Linear Scale'), ('date_picker', 'Date Picker'), ('time_picker', 'Time Picker'), ('file_upload', 'File Upload'), ('matrix_grid', 'Matrix/Grid'), ('image_choice', 'Image Choice'), ('slider', 'Slider'), ('signature_capture', 'Signature Capture'), ('color_picker', 'Color Picker'), ('geolocation', 'Geolocation'), ('percentage_allocation', 'Percentage Allocation')], max_length=50)),
                ('order', models.PositiveIntegerField()),
                ('min_value', models.IntegerField(blank=True, null=True)),
                ('max_value', models.IntegerField(blank=True, null=True)),
                ('is_required', models.BooleanField(default=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='forms.form')),
            ],
            options={
                'db_table': 'forms_question',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='forms.question')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='forms.form')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='answers/')),
                ('image_choice', models.ImageField(blank=True, null=True, upload_to='image_choices/')),
                ('slider_value', models.IntegerField(blank=True, null=True)),
                ('ranking_value', models.IntegerField(blank=True, null=True)),
                ('geolocation_value', models.CharField(blank=True, max_length=255, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='forms.response')),
            ],
            options={
                'db_table': 'forms_answer',
            },
        ),
    ]
