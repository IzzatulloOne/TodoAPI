from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=177)
    description = models.TextField()
    complited = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)