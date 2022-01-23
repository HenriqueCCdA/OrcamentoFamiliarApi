from django.db import models

# Create your models here.

class Base(models.Model):

    class Meta:
        abstract = True

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao


class Receita(Base):
    pass

class Despesa(Base):
    pass
