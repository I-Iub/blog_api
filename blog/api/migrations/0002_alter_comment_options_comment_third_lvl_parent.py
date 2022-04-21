# Generated by Django 4.0.4 on 2022-04-21 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='comment',
            name='third_lvl_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farther_comments', to='api.comment', verbose_name='Предок третьего уровня'),
        ),
    ]
