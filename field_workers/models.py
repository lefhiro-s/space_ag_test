from django.db import models


class FieldWorker(models.Model):

    class Function(models.TextChoices):
        Harvest = 'Harvest'
        Pruning = 'Pruning'
        Scouting = 'Scouting'
        Other = 'Other'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    function = models.CharField(max_length=50, choices=Function.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "field workers"
