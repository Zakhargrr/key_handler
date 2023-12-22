from django.db import models


# Create your models here.


class Secret(models.Model):
    secret_string = models.CharField(max_length=30, verbose_name='секретная строка')
    code_phrase = models.CharField(max_length=70, verbose_name='кодовая фраза')
    secret_key = models.CharField(max_length=70, null=True, blank=True, verbose_name='секретный ключ')
    counter = models.IntegerField(default=0, verbose_name='счетчик')

    class Meta:
        verbose_name = 'секрет'
        verbose_name_plural = 'секреты'
