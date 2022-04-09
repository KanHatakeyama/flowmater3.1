# Generated by Django 4.0.3 on 2022-03-30 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_graph_created_at_graph_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='tags',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='graph',
            name='graph',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
    ]
