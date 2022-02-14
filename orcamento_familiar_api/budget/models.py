from datetime import datetime
from decimal import Decimal

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

    def to_dict(self, id_field=True):

        dict_ = {
            'descricao': self.descricao,
            'valor': str(self.valor),
            'data': str(self.data)
        }

        if id_field:
            dict_['id'] = self.id

        return dict_

    @classmethod
    def dict_to_model(cls, dict_):
        date = datetime.fromisoformat(dict_['data'])
        return cls(descricao=dict_['descricao'].strip(),
                   valor=Decimal(dict_['valor']),
                   data=date,
                   mes=date.month)

    def check_restriction_create(self):
        model = self.__class__
        return not model.objects.filter(descricao=self.descricao,
                                        data__month=self.data.month).exists()

    def check_restriction_update(self):
        model = self.__class__

        exist_obj = model.objects.filter(descricao=self.descricao,
                                         data__month=self.data.month).first()

        if not exist_obj:
            return True

        return self.id == exist_obj.id


class Receita(Base):
    pass


class Despesa(Base):
    pass
