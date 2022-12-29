# Generated by Django 4.0.4 on 2022-12-26 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerrytq', '0016_projectcredittoproject_remove_project_credits_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLinkToProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('image_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.imagelink')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TechnologyToProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='image_links',
        ),
        migrations.AddField(
            model_name='project',
            name='image_links',
            field=models.ManyToManyField(through='jerrytq.ImageLinkToProject', to='jerrytq.imagelink'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='technologies',
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(through='jerrytq.TechnologyToProject', to='jerrytq.technology'),
        ),
        migrations.AddField(
            model_name='technologytoproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.project'),
        ),
        migrations.AddField(
            model_name='technologytoproject',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.technology'),
        ),
        migrations.AddField(
            model_name='imagelinktoproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jerrytq.project'),
        ),
    ]