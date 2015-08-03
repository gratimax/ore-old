from django.db import models

class Nonce(models.Model):
    nonce = models.CharField(max_length=128, unique=True, null=False, blank=False)
