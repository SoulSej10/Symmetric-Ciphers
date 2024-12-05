from django.db import models

# Create your models here.
from django.db import models

class CaesarCipherData(models.Model):
    text = models.TextField()
    shift = models.IntegerField()
    result = models.TextField()
    operation = models.CharField(max_length=10)  # "encrypt" or "decrypt"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation} at {self.timestamp}"



