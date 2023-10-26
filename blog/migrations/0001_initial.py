from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('content', models.TextField(verbose_name='содержимое статьи')),
                ('img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение')),
                ('count_views', models.IntegerField(blank=True, default=0, null=True, verbose_name='количество просмотров')),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='дата публикации')),
                ('is_published', models.BooleanField(blank=True, default=True, null=True, verbose_name='опубликовано')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
            },
        ),
    ]
