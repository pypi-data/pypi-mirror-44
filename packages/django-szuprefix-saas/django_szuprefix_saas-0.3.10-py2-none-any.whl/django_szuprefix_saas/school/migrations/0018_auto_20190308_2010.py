# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-08 12:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0017_auto_20190126_2328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clazzcourse',
            options={'verbose_name': '\u73ed\u7ea7\u8bfe\u7a0b', 'verbose_name_plural': '\u73ed\u7ea7\u8bfe\u7a0b'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ('party', '-create_time'), 'permissions': (('view_teacher', '\u67e5\u770b\u8001\u5e08\u8d44\u6599'),), 'verbose_name': '\u8001\u5e08', 'verbose_name_plural': '\u8001\u5e08'},
        ),

        migrations.AlterField(
            model_name='clazzcourse',
            name='clazz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clazz_course_relations', to='school.Clazz', verbose_name='\u73ed\u7ea7'),
        ),
        migrations.AlterField(
            model_name='clazzcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clazz_course_relations', to='course.Course', verbose_name='\u8bfe\u7a0b'),
        ),
        migrations.AlterField(
            model_name='clazzcourse',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clazz_course_relations', to='school.Teacher', verbose_name='\u8001\u5e08'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_school_teacher', to=settings.AUTH_USER_MODEL, verbose_name='\u7f51\u7ad9\u7528\u6237'),
        ),
         migrations.AlterField(
            model_name='clazz',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='school_classes', through='school.ClazzCourse', to='course.Course', verbose_name='\u8bfe\u7a0b'),
        ),
    ]
