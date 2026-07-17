from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_important = models.BooleanField(default=False, verbose_name="Важная")

    def __str__(self):
        return self.title