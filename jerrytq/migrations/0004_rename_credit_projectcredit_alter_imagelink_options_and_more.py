# Generated by Django 4.0.4 on 2022-11-06 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jerrytq', '0003_alter_project_options_remove_project_end_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Credit',
            new_name='ProjectCredit',
        ),
        migrations.AlterModelOptions(
            name='imagelink',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='projectcredit',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='projectlink',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='imagelink',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectlink',
            name='project',
        ),
        migrations.AddField(
            model_name='imagelink',
            name='name',
            field=models.CharField(default='test', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='image_link',
            field=models.ManyToManyField(to='jerrytq.imagelink'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_link',
            field=models.ManyToManyField(to='jerrytq.projectlink'),
        ),
    ]