# Proxy Search
##### Prototipo ideato per la ricerca dinamica di dati all'interno di un database relazionale.
## Descrizione
*Proxy Search* si occupa di interfacciarsi con *Metabase*, 
al fine di ottenere i risultati di ricerca richiesti attraverso l'api che mette a disposizione, tramite il supporto di un database contenenti le informazioni per il mapping.

## Funzionalità principali
* ricerca di valori all'interno di un database relazionale

## Struttura del progetto
Il progetto è realizzato in Django mediante Python v. 3.8 ed è caratterizzato dal Package principale **ProxySearch**.
Utilizza un database di tipo sqlite su cui vengono memorizzate le informazioni per il mapping.

###ProxySearch
contiene il file per l'avvio della piattaforma di sviluppo [wsgi](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/),
il file di settings contenente le configurazioni per django del progetto, gli schemi utilizzati da swagger per la visualizzazione delle api, 
####Package interni 
 * il package **api** contenente le rotte dell'applicazione
 * il package **utils** contentente tutte le funzionalità utilizzate implementate nel progetto.

## Requisiti
* Occorre avere una istanza attiva di Metabase a cui bisogna avere collegato almeno un database di riferimento.
* *Proxy Search* necessita delle seguenti librerie:
    * PyYAML              | versione 5.4.1
    * django              | versione 3.2.6
    * djangorestframework | versione 3.12.4
    * drf-yasg            | versione 1.20.0
    * requests            | versione 2.26.0
    * uritemplate         | versione 3.0.1

## Utilizzo
Al momento viene esposta solo una api che restituisce i valori attesi indicando i seguenti parametri:
* tableName -> nome della tabella in cui effettuare la ricerca.
* filters -> lista dei filtri che si desidera applicare, ogni filtro è caratterizzato da:
  * fieldName -> nome del campo su cui applicare il filtro
  * dataType -> tipo di dato che è contenuto in quel campo
  * filterType -> tipo di confronto applicato dal filtro
  * value -> termine di paragone per il filtr

## Accesso alle API
 * **/swagger**
   lista delle api all'interno di swagger
 * **/research** 
Inviando come parametri il riferimento alla tabella su cui ricercare e la lista dei filtri che si desidera applicare, 
   viene restituita una lista dei risultati relativi ai valori ricercati.

## Installazione
 *Proxy Search* non presenta una procedura di installazione
 ma si appoggia ad una instanza di [Metabase](https://www.metabase.com/docs/latest/operations-guide/installing-metabase.html).

## Build system, CI e test automatici
 Per avviare il progetto lanciare la procedura Start.sh

## Project status
 *Proxy Search* è un prototipo, in stato alpha, aperto a nuovi sviluppi
## Copyright
 *Proxy Search* non dispone di alcun Copyright
