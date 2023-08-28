from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Chat(models.Model):
    content = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
