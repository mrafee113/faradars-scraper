# Generated by Django 4.0 on 2022-09-20 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('link', models.URLField()),
            ],
            options={
                'unique_together': {('name', 'link')},
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('faradars', 'faradars')], max_length=100)),
                ('title', models.TextField()),
                ('link', models.URLField()),
                ('number_of_students', models.IntegerField(default=-1)),
                ('duration', models.DurationField(null=True)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.tutor')),
            ],
        ),
    ]
