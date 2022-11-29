from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todoss(models.Model):
    task_name=models.CharField(max_length=200)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task_name