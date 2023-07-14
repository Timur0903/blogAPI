from django.db import models

# Create your models here.
from django.db import models

class Categorys(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User',
                              related_name='to_do', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title