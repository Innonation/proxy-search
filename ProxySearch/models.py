from django.db import models


class MappingTable(models.Model):
    idTable = models.AutoField(primary_key=True)
    tableName = models.CharField(verbose_name='Nomi delle tebelle', max_length=50)


class MappingField(models.Model):
    idField = models.AutoField(primary_key=True)
    fieldName = models.CharField(verbose_name='Nomi dei campi', max_length=50)
    idTable = models.ForeignKey(MappingTable, verbose_name='Mapping ID', on_delete=models.RESTRICT)
