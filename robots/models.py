from django.db import models
from django.utils import timezone



class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    available = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Убедитесь, что created имеет правильную временную зону перед сохранением
        if not self.created.tzinfo:
            self.created = timezone.make_aware(self.created)

        super(Robot, self).save(*args, **kwargs)


    def __str__(self):
        return self.model

