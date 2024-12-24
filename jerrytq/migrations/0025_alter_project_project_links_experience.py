# Generated by Django 4.1 on 2024-12-24 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jerrytq", "0024_alter_skill_options_skill_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="project_links",
            field=models.ManyToManyField(blank=True, to="jerrytq.projectlink"),
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=32)),
                ("company", models.CharField(max_length=32)),
                ("location", models.CharField(max_length=32)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "image_link",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="jerrytq.imagelink",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]