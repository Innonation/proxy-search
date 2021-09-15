import json
import logging
import requests

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import viewsets, status

# from ProxySearch.api.responses_schema import ItemViewSetListSchema
from rest_framework.decorators import api_view

from ProxySearch.schemas import DoQueryResponseSchema, DoMetadataResponseSchema, \
    DoQueryBodySchema
from ProxySearch.utils.Choices import EndpointMetabase
from ProxySearch.utils.utils import mapValues, makeResponse
from ProxySearch.utils.utils_db import fillDatabase, translateField, translateTable


LOG = logging.getLogger(__name__)


def retrieveAuthCookies(username=None, password=None):
    """
    Autenticazione Metabase
    """
    url = settings.METABASE_URL + EndpointMetabase.AUTH.value
    payload = {'username': username, 'password': password}

    try:
        LOG.info("Api: {}".format(url))
        response = requests.post(url=url, json=payload, headers={"Content-Type": "application/json"})
        return response.cookies
    except Exception as e:
        print(e)
        LOG.warning("Exception: {}".format(str(e)))


def retrieveMetadataInfo(authCookies):
    """
    Recupera i metadati per il riempimento iniziale delle tabelle.
    :param authCookies: Cookies di autenticazione
    :return: Response
    """
    url = settings.METABASE_URL + EndpointMetabase.METADATA.value

    try:
        LOG.info("Api: {}".format(url))
        response = requests.get(url=url, cookies=authCookies)
        return response.text
    except Exception as e:
        print(e)
        LOG.warning("Exception: {}".format(str(e)))


def retrieveQueryMetadataInfo(authCookies, table_id):
    """
    Recupera i metadati nel caso di query che coinvolgono chiavi esterne.
    :param authCookies: Cookies di autenticazione
    :param table_id: ID della tabella
    :return: response
    """
    url = settings.METABASE_URL + "table/" + str(table_id) + "/query_metadata"

    try:
        LOG.info("Api: {}".format(url))
        response = requests.get(url=url, cookies=authCookies)
        return response.text
    except Exception as e:
        print(e)
        LOG.warning("Exception: {}".format(str(e)))


def callMetabaseDatasetApi(json_payload):
    url = settings.METABASE_URL + 'dataset'
    cookies = retrieveAuthCookies("M.Rossi@innonation.it", "Test123!")
    response = requests.post(url=url, cookies=cookies, json=json_payload, headers={"Content-Type": "application/json"})
    return response


def retrieveForeignTableID(table_id, source_field_id):
    """
    Recupera l'ID della tabella della chiave esterna.
    :param table_id: ID della tabella
    :param source_field_id: ID del campo
    :return: ID della tabella della chiave esterna
    """
    queryMetadataText = retrieveQueryMetadataInfo(retrieveAuthCookies("M.Rossi@innonation.it", "Test123!"), table_id)
    queryMetadataJSON = json.loads(queryMetadataText)
    fields = queryMetadataJSON['fields']
    foreign_table_id = 0
    for field in fields:
        if field['id'] == source_field_id:
            foreign_table_id = field['target']['table_id']
    return foreign_table_id


def getForeignInfo(table_id, field_name, source_field_name):
    source_field_id = translateField(source_field_name, table_id)
    foreign_table_id = retrieveForeignTableID(table_id, source_field_id)
    field_id = translateField(field_name, foreign_table_id)
    return field_id, source_field_id


def makeQueryDetails(filter, table_id):
    query_details = []
    query_details.append("field")
    if 'sourceFieldName' in filter:
        field_id, source_field_id = getForeignInfo(table_id, filter['fieldName'], filter['sourceFieldName'])
        query_details.append(field_id)
        query_details.append({"source-field": source_field_id})
    else:
        query_details.append(translateField(filter["fieldName"], table_id))
        query_details.append("")
    return query_details


def makeFilterElement(filter, query_details):
    filter_element = []
    filter_element.append(filter["filterType"])
    filter_element.append(query_details)
    filter_element.append(filter["value"])
    return filter_element


def getFilterElement(filter, table_id):
    query_details = makeQueryDetails(filter, table_id)
    filter_element = makeFilterElement(filter, query_details)
    return filter_element


class FieldViewSet(viewsets.ViewSet):
    @swagger_auto_schema(method='post', description="avvia la raccolta dei metadati", responses=DoMetadataResponseSchema)
    @api_view(['POST'])
    def doMetadata(self, request):
        """
        API che avvia la raccolta dei metadati.
        """
        try:
            if not 'X-Metabase-Session' in request.COOKIES:
                return JsonResponse({'message': DoQueryResponseSchema[status.HTTP_401_UNAUTHORIZED].get('description')},
                                    status=status.HTTP_401_UNAUTHORIZED)

            metadataText = retrieveMetadataInfo(retrieveAuthCookies("M.Rossi@innonation.it", "Test123!"))
            metadataJSON = json.loads(metadataText)
            tables, fields = mapValues(metadataJSON)
            fillDatabase(tables, fields)
            return HttpResponse("Ok")
        except Exception as e:
            print(e)
            LOG.warning("Exception: {}".format(str(e)))
            return JsonResponse(
                {'message': DoQueryResponseSchema[status.HTTP_500_INTERNAL_SERVER_ERROR].get('description')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(method='post', description="avvia l'interrogazione a Metabase in base ai parametri passati", request_body=DoQueryBodySchema, responses=DoQueryResponseSchema)
    @api_view(['POST'])
    def doQuery(self, request):
        """
        Api che avvia l'interrogazione a Metabase in base ai parametri passati.
        """
        try:
            if not 'X-Metabase-Session' in request.COOKIES:
                return JsonResponse({'message': DoQueryResponseSchema[status.HTTP_401_UNAUTHORIZED].get('description')},
                                    status=status.HTTP_401_UNAUTHORIZED)
            json_data = json.loads(request.body)
            if not all(param in json_data.keys() for param in ['tableName','filters']):
                return JsonResponse({'message': DoQueryResponseSchema[status.HTTP_403_FORBIDDEN].get('description')}, status=status.HTTP_403_FORBIDDEN)
            filters = json_data['filters']
            table_name = json_data['tableName']
            table_id = translateTable(table_name)

            current_filters = []

            if filters.__len__() > 1:
                current_filters.append("and")
                for filter in filters:
                    filter_element = getFilterElement(filter, table_id)
                    current_filters.append(filter_element)
            else:
                value = filters[0]['value']
                filter_type = filters[0]['filterType']
                field_name = filters[0]['fieldName']
                field_id = translateField(field_name, table_id)
                current_filters = [filter_type, ["field", field_id, ""], value]
                if 'sourceFieldName' in filters[0]:
                    field_id, source_field_id = getForeignInfo(table_id, field_name, filters[0]['sourceFieldName'])
                    current_filters[1][1] = field_id
                    current_filters[1][2] = {"source-field": source_field_id}

            json_payload = {
                "type": "query",
                "query": {
                    "source-table": table_id,
                    "filter": current_filters
                },
                "database": 2,
                "parameters": []
            }

            metabase_response = callMetabaseDatasetApi(json_payload)
            jsonResponseObject = json.loads(metabase_response.text)
            response = makeResponse(jsonResponseObject)
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            LOG.warning("Exception: {}".format(str(e)))
            return JsonResponse({'message': DoQueryResponseSchema[status.HTTP_500_INTERNAL_SERVER_ERROR].get('description')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # return Response(ItemViewSetListSchema['400'].description, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
