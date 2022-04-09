# Generated by Django 4.0.3 on 2022-03-30 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0004_graph_tags_alter_graph_graph'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploaded/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]