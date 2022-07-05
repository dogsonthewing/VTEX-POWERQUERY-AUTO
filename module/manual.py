import json
import time
import modules.logger as log
from datetime import datetime
from modules.ETL import newOrders , updateOrders
from modules.config import setConfig
from modules.emailsender import sendEmail
from modules.decrypter import decryptJson
from modules.logger import log


def run():
    # jsonConfigFile = decryptJson('config/config.json' , 'config/config.key')
    # config = json.loads(jsonConfigFile)
    jsonConfigFile = open('config/configurat.json')
    config = json.load(jsonConfigFile)

    
    #Ao rodar manualmente não esqueça de alterar as datas a serem puxadas no ETL.py, se necessário
    start_time = time.time()
    log.infoLog()
    setConfig(config['willerk'])
    newOrders()
    updateOrders()
    #sendEmail('Sucesso.')
    log.infoLog("Store updated in %s seconds" % (time.time() - start_time))

    jsonConfigFile.close()

    return