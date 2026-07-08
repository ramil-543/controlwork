from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата выполнения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
    
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)

    def _str_(self):
        return self.title

    class Meta:
        ordering = ['-created_at']