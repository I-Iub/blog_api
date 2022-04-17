from django.db import models


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title[:50]


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )
    level = models.PositiveIntegerField('Вложенность')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Родительский комментарий'
    )
    text = models.TextField('Текст')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Статья: {self.article}, id: {self.id}'
