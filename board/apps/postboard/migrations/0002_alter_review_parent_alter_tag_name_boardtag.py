# Generated by Django 4.0 on 2022-03-11 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='postboard.review'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='BoardTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postboard.board')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postboard.tag')),
            ],
        ),
    ]
