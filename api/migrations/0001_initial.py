# Generated by Django 4.0.4 on 2022-04-15 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HKU_ID', models.CharField(max_length=10, unique=True)),
                ('Name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Venue_Code', models.CharField(max_length=20, unique=True)),
                ('Location', models.CharField(max_length=150)),
                ('Type', models.CharField(max_length=2)),
                ('Capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PositiveCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Of_Diagonsis', models.DateField()),
                ('HKU_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.member')),
            ],
        ),
        migrations.CreateModel(
            name='AccessRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Time', models.DateTimeField()),
                ('Action', models.CharField(max_length=5)),
                ('HKU_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.member')),
                ('Venue_Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.venue')),
            ],
        ),
    ]
