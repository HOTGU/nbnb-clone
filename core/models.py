from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    objects = managers.CurstomModelManagers()

    class Meta:
        abstract = True
