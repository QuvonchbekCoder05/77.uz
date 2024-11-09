

from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=128)
    region = models.ForeignKey(Region, related_name="districts", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Page(models.Model):
    slug = models.SlugField(unique=True)
    content = models.TextField()

    def __str__(self):
        return self.slug
