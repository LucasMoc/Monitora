from django.db import models
from django.core.validators import MinValueValidator


class monitoringStock(models.Model):
    stock = models.CharField('Ativos',
                             max_length=15)
    value_max = models.DecimalField('Túnel máx.',
                                    max_digits=10,
                                    decimal_places=2)
    value_min = models.DecimalField('Túnel mín.',
                                    max_digits=10,
                                    decimal_places=2,
                                    validators=[MinValueValidator(0.001, 'Túnel míx. deve ser maior que R$ 0,00.')])

    moniTime = models.IntegerField('Tempo de checagem em horas',
                                   validators=[MinValueValidator(1, 'Periodicidade deve ser no mínimo de 1 hora.')])

    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.stock


class historyMonitoring(models.Model):
    stock = models.CharField('Código do ativo', max_length=15)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField('Data de atualização')
    email = models.EmailField(max_length=255)
    monistock = models.ForeignKey(
        monitoringStock, on_delete=models.CASCADE, null=True)
