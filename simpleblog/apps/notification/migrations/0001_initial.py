# Generated by Django 2.0.7 on 2020-02-23 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上线')),
                ('order', models.IntegerField(default=0, verbose_name='排序顺序')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('content', models.CharField(max_length=64, verbose_name='通知内容')),
            ],
            options={
                'verbose_name': '通知表',
                'verbose_name_plural': '通知表',
                'db_table': 'myblog_notification',
            },
        ),
    ]
