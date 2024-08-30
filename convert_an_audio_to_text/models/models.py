from django.db import models

class NumberChoicesModel(models.TextChoices):
    tiny_en = 'tiny.en'
    tiny = 'tiny'
    base_en = 'base.en'
    base = 'base'
    small_en = 'small.en'
    small = 'small'
    medium_en = 'medium.en'
    medium = 'medium'
    large_v1 = 'large-v1'
    large_v2 = 'large-v2'
    large_v3 = 'large-v3'
    large = 'large'

class AudioToTextModel(models.Model):
    audio_file = models.FileField(upload_to='voices', null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text='Выберите аудио файл, только mp3/wav')
    text_of_file = models.TextField(null=True, blank=True)
    choose_model = models.CharField(choices=NumberChoicesModel.choices)
