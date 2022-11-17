# Generated by Django 3.0.3 on 2020-12-28 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spin', '0022_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spin.InventoryItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spin.User')),
            ],
            options={
                'ordering': ['user', 'item'],
            },
        ),
    ]