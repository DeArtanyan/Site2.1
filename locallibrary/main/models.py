from django.db import models
from django.contrib.auth.models import User

class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=[
        ('3D', '3D дизайн'),
        ('2D', '2D дизайн'),
        ('sketch', 'Эскиз')
    ])
    photo = models.ImageField(upload_to='design_requests/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title