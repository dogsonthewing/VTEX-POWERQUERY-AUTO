import json
import time
from datetime import datetime
from modules.ETL import newOrders , updateOrders
from modules.config import setConfig
from modules.emailsender import sendEmail
from modules.decrypter import decryptJson
from modules.logger import infoLog

# jsonConfigFile = open('config/configurat.json')
# config = json.load(jsonConfigFile)
# jsonConfigFile.close()

def run():
    main_time = time.time()
    jsonConfigFile = decryptJson('config/c.json' , 'config/f.key')
    config = json.loads(jsonConfigFile)
    storeCounter = 0
    newOrdersCounter = 0
    
    for store in config:
        store_time = time.time()
        infoLog(str(datetime.today()) + " " + store + " started")
        print('------------------------')
        print(store)
        setConfig(config[store])
        newOrdersCounter = newOrdersCounter + int(newOrders())
        updateOrders()
        infoLog(str(datetime.today()) + " -- " + store + " complete in %s seconds" % (time.time() - store_time))
        storeCounter = storeCounter + 1
    
    infoLog(str(datetime.today()) + " Complete automatization runned in %s seconds" % (time.time() - main_time))
    processTime = time.time() - main_time
    
    sendEmail("""\
    Subject: Automatização VTEX

    Lojas VTEX atualizadas com sucesso: {}/6 
    Total de pedidos inseridos no Big Query: {}
    Tempo de processo: {} segundos""".format(storeCounter,newOrdersCounter,processTime).encode('utf-8'))

    return