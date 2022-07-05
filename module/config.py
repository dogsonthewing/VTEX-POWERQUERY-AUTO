import os
import ast
from google.cloud import bigquery
from datetime import datetime , timedelta

credentials_path = 'H:\Meu Drive\VTEX-POWERQUERY-AUTO\DEV\config\sa.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

def setConfig(config):
    headers = {}
    headers = ast.literal_eval(config['headers'])
    table_id = config['table_id']
    url = config['url']    

    setGlobalConfig(table_id , headers , url)
    return url

def setGlobalConfig(table , headersConfig , currentUrl):
    global client
    global headers
    global table_id
    global url
    global generalUrl

    client = bigquery.Client()
    table_id = table
    headers = headersConfig
    url = currentUrl
    generalUrl = currentUrl

    return

#first e last são, respectivamente, de quantos dias atrás até qual dia atrás deve ser puxado
def setExtractionDate(currentUrl , first , last):
    global url
    url = currentUrl + "/api/oms/pvt/orders?f_creationDate=creationDate:%5B{lastdate}T00:00:00.001Z%20TO%20{date}T23:59:59.999Z%5D&orderBy=creationDate,asc&per_page=100&".format(lastdate = str(datetime.today() - timedelta(first))[:10] , date = str(datetime.today() - timedelta(last))[:10])
    url = url + "page={npage}"
    return