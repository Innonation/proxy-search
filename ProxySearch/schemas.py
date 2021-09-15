from drf_yasg import openapi
from rest_framework.status import *

DoMetadataParameters = [openapi.Parameter('databaseId', openapi.IN_PATH, description="identificativo del database", type=openapi.TYPE_INTEGER)]
DoMetadataResponseSchema = {HTTP_200_OK: openapi.Response(
        description="Ok"), HTTP_403_FORBIDDEN: openapi.Response(
        description='utente non autorizzato'), HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(description='Si è verificato un errore interno.')}


DoQueryBodySchema = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, required=['tableName', 'filters'], properties={
                'tableName': openapi.Schema(description='Nome della tabella su cui ricercare', type=openapi.TYPE_STRING),
                'filters':openapi.Schema(description='Lista di filtri da applicare nella ricerca', type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                    'fieldName': openapi.Schema(description='Nome del campo della tabella', type=openapi.TYPE_STRING),
            'dataType': openapi.Schema(description='Tipo di dato associato al campo', type=openapi.TYPE_STRING),
            'filterType': openapi.Schema(description='Tipo di confronto da operare per applicare il filtro', type=openapi.TYPE_STRING),
            'value': openapi.Schema(description='Valore di riferimento per il filtro', type=openapi.TYPE_STRING),
            'sourceFieldName': openapi.Schema(description='Tipo di dato associato al campo', type=openapi.TYPE_STRING),
                }))}))

DoQueryResponseSchema = {HTTP_200_OK: openapi.Response(
        description="Risposta attesa", examples={'fields': 'array dei campi', 'rows': 'lista contenente l\'array dei valori'}), HTTP_403_FORBIDDEN: openapi.Response(
        description='utente non autorizzato'), HTTP_400_BAD_REQUEST:  openapi.Response(description='parametri di ricerca non validi'), HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
        description='Si è verificato un errore interno.')}