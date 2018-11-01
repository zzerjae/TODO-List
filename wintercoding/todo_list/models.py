from django.conf import settings
from django.db import models


class TODO(models.Model):
    STATUS_CHOCES = (
        ('i', '진행중'),
        ('c', '완료'),
        ('e', '기한 초과'),
    )

    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', related_name='created_by',
        on_delete=models.CASCADE)
    status = models.CharField(max_length=1, verbose_name='상태', choices=STATUS_CHOCES, default='i')
    completed_at = models.DateTimeField(verbose_name='완료 일자', blank=True, null=True)
    due_date = models.DateField(verbose_name='마감 날짜', blank=True, null=True)
    due_time = models.TimeField(verbose_name='마감 시간', blank=True, null=True)
    priority = models.PositiveIntegerField(verbose_name='우선순위')

    class Meta:
        ordering = ['priority']

    def is_completed(self):
        return self.status == 'c'

    def __str__(self):
        return self.title