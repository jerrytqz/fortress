# Generated by Django 4.0.4 on 2022-12-22 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerrytq', '0014_alter_skill_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['technology__name']},
        ),
        migrations.RemoveField(
            model_name='skill',
            name='image_link',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='name',
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('type', models.CharField(choices=[('LAN', 'Language'), ('FRA', 'Framework'), ('LIB', 'Library'), ('TOO', 'Tool')], default='LAN', max_length=3)),
                ('image_link', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jerrytq.imagelink')),
            ],
            options={
                'verbose_name_plural': 'technologies',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='skill',
            name='technology',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jerrytq.technology'),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(to='jerrytq.technology'),
        ),
    ]
