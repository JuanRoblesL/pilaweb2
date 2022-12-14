from django.db import models

# Create your models here.
class Categorias(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Productos(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    relese_year = models.BigIntegerField()
    categorie = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    #image = models.BinaryField()
    def __str__(self):
        return self.name

class Comentarios(models.Model):
    comment = models.CharField(max_length=600)
    author = models.CharField(max_length=100)
    date = models.DateField()
    product = models.ForeignKey(Productos, on_delete=models.CASCADE)

    def __str__(self):
        str = "%s   |   %s  |   %s" % (self.product, self.comment, self.date)
        return str