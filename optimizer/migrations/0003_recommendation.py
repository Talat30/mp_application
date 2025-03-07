# Generated by Django 5.1.6 on 2025-03-02 12:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optimizer', '0002_delete_recommendation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_date', models.DateTimeField(auto_now_add=True)),
                ('watched', models.BooleanField(default=False)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizer.netflixshow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
