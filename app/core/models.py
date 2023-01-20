from djongo import models


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    number = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Recipe(models.Model):
    index = models.PositiveBigIntegerField(unique=True)
    title = models.CharField(max_length=300)
    ingredients = models.ArrayField(model_container=Ingredient)
