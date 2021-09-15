from ProxySearch.utils.utils_db import getFieldNameById


def mapValues(metadataJSON):
    """
    Mappa i valori dei metadati.
    :param metadataJSON:
    :return:
    """
    tables = {}
    for table in metadataJSON['tables']:
        tables[table['id']] = table['name']

    fields = {}
    for table in metadataJSON['tables']:
        for field in table['fields']:
            fields[field['id']] = [field['name'], field['table_id']]

    return tables, fields


def extractFields(jsonResponseObject):
    cols = jsonResponseObject["data"]["cols"]
    fields = []
    for col in cols:
        field_id = col['id']
        table_id = col['table_id']
        field_name = getFieldNameById(field_id, table_id)
        fields.append(field_name)
    return fields


def makeResponse(jsonResponseObject):
    response = {}
    response["fields"] = extractFields(jsonResponseObject)
    response["rows"] = jsonResponseObject["data"]["rows"]
    return response
