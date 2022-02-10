from django.db import models


class Base(models.Model):

    class Meta:
        abstract = True
        unique_together = ('descricao', 'mes',)

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()
    mes = models.IntegerField()
    criacao = models.DateTimeField(auto_now_add=True)
    modificacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

    @staticmethod
    def required_fields():
        return ('descricao', 'valor', 'data')

    def to_dict(self):
        return {
            'descricao': self.descricao,
            'valor': self.valor,
            'data': self.data
        }


class Receita(Base):
    pass


class Despesa(Base):
    pass
