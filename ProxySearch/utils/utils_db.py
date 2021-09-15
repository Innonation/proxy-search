import logging

from ProxySearch.models import MappingTable, MappingField


LOG = logging.getLogger(__name__)


def fillDatabase(tables, fields):
    try:
        for idTable, tableName in tables.items():
            table = MappingTable(idTable=idTable, tableName=tableName)
            table.save()
            for idField, info in fields.items():
                if idTable == info[1]:
                    field = MappingField(idField=idField, fieldName=info[0], idTable=table)
                    field.save()
    except Exception as e:
        print(e)
        LOG.warning("Exception: {}".format(str(e)))


def translateTable(table_name):
    """
    Traduzione del nome della tabella con il suo ID.
    :param table_name: Nome della tabella
    :return: ID della tabella
    """
    try:
        mapping_table = MappingTable.objects.filter(tableName=table_name).values("idTable").first()
        if mapping_table:
            return mapping_table["idTable"]
        else:
            return None
    except Exception as e:
        LOG.warning("Exception: {}".format(str(e)))


def translateField(field_name, table_id):
    """
    Traduzione del nome del campo con il suo ID.
    :param field_name: Nome del campo
    :param table_id: ID della tabella
    :return: ID del campo
    """
    try:
        mapping_field = MappingField.objects.filter(fieldName=field_name, idTable=table_id).values("idField").first()
        if mapping_field:
            return mapping_field["idField"]
        else:
            return None
    except Exception as e:
        LOG.warning("Exception: {}".format(str(e)))


def getFieldNameById(field_id, table_id):
    """
    Traduzione dell'ID del campo con il suo nome.
    :param field_id: ID del campo
    :param table_id: ID della tabella
    :return: Nome del campo
    """
    try:
        mapping_field = MappingField.objects.filter(idField=field_id, idTable=table_id).values("fieldName").first()
        if mapping_field:
            return mapping_field["fieldName"]
        else:
            return None
    except Exception as e:
        LOG.warning("Exception: {}".format(str(e)))
