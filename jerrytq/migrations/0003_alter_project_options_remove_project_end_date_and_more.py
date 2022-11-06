# Generated by Django 4.0.4 on 2022-11-06 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerrytq', '0002_rename_credits_credit_rename_projects_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='project',
            name='end_date',
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('url', models.URLField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.project')),
            ],
            options={
                'ordering': ['project'],
            },
        ),
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.project')),
            ],
            options={
                'ordering': ['project'],
            },
        ),
    ]
