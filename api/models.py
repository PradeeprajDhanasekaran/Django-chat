from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    thread_name= models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content}"
