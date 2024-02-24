from django.db import models


class Recipe(models.Model):
    index = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=300)
    process = models.TextField(default="")
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    number = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("recipe", "name")


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
