# Generated by Django 4.0.2 on 2022-02-15 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='questions_text',
            new_name='question_text',
        ),
    ]
