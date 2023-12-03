from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, unique=True, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_image/', verbose_name='превью', **NULLABLE)
    date_creation = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    is_publication = models.BooleanField(verbose_name='Опубликовано')
    number_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'

