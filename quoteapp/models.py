from django.db import models
from django.utils import timezone


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50, unique=True, null=False)
    born_date = models.DateTimeField(default=timezone.now)
    born_location = models.CharField(max_length=150, null=False)
    description = models.CharField(null=False)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.CharField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
