import requests
import time
import modules.logger as log
import modules.config as config
from datetime import datetime
from modules.CRUD import insertOrders , read, update
from collections import defaultdict

#Lê cada página e retorna uma lista com os pedidos concatenados de todas as páginas
def extractOrders():
    start_time = time.time()
    page = 1
    orderCount = 100
    completeorders = []

    while orderCount == 100:
        url = config.url.format(npage = page)
        orders = requests.get(url, headers=config.headers)
        orders = orders.json()
        orders = orders['list']
        completeorders.extend(orders)
        page = page + 1
        orderCount = len(orders)

    print('Data was successfully extracted.')
    log.infoLog(str(datetime.today()) + " -- Extraction complete in %s seconds" % (time.time() - start_time))
    return completeorders

#Faz a tratativa de pedido por pedido
def treatOrdersInsertion(orders):
    start_time = time.time()
    counter = 0
    completeorders = []
    for order in orders:
        if str(order['marketPlaceOrderId']) == 'None':
            counter = counter + 1
            utmSource = getUTM(order['orderId'])
            order['orderId'] = str(order['orderId'])[:-3]
            order['creationDate'] = order['creationDate'][:19].replace('T' , ' ')
            order['totalValue'] = str(order['totalValue'])[:-2] #remove o .0 do valor
            order['totalValue'] = str(order['totalValue'])[:-2] + '.' + str(order['totalValue'])[-2:] #separa reais de centavos
            data_set = [{"orderId": order['orderId'] , "creationDate": order['creationDate'] , "status": order['status'] , "totalValue": order['totalValue'] , "paymentNames": order['paymentNames'] , "utmSource" : utmSource }]
            completeorders.extend(data_set) 
    print('Data was successfully treated. ' + str(counter) + ' orders.')
    log.infoLog(str(datetime.today()) + " -- orders treated for INSERTION in %s seconds" % (time.time() - start_time))
    return completeorders

def getUTM(orderId):
    orderUrl = config.generalUrl + '/api/oms/pvt/orders/' + orderId
    order = requests.get(orderUrl, headers=config.headers)
    order = order.json()
    if order['marketingData'] != None:
        return order['marketingData']['utmSource']
    return 

def treatOrdersUpdate(orders):
    start_time = time.time()
    completeorders = []
    counter = 0
    for order in orders:
        if str(order['marketPlaceOrderId']) == 'None':
            counter = counter + 1
            order['orderId'] = str(order['orderId'])[:-3]
            data_set = [{"orderId": order['orderId'] , "status": order['status']}]
            completeorders.extend(data_set)
    print('Data was successfully treated. ')
    log.infoLog(str(datetime.today()) + " -- orders treated for UPDATE in %s seconds" % (time.time() - start_time))
    return completeorders

#Carrega os pedidos em formato de LISTA para serem inseridos através do insertOrders()
def loadList(orders):
    start_time = time.time()
    counter = 0
    print('Loading data into Big Query.')
    for order in orders:
        counter = counter + int(insertOrders(order['orderId'] , order['creationDate'] , order['status'] , order['totalValue'] , order['paymentNames'] , order['utmSource']))
    print('Data was successfully loaded.')
    log.infoLog(str(datetime.today()) + " -- " + str(counter) + " orders inserted in %s seconds" % (time.time() - start_time))
    return counter

def newOrders():
    config.setExtractionDate(config.generalUrl , 1 , 1)
    orders = treatOrdersInsertion(extractOrders())
    newOrders = str(loadList(orders))
    print(newOrders + ' New orders')
    return newOrders

def updateOrders():
    config.setExtractionDate(config.generalUrl , 15 , 1)
    vtexOrders = treatOrdersUpdate(extractOrders())
    start_time = time.time()
    orderId = ''
    orderUpadateList = defaultdict(list)
    statusList = []
    counter = 0
    #cria a consulta com os parametros dos chamados da vtex
    for vtexOrder in vtexOrders:
        orderId = orderId + str("'{}' , ".format(vtexOrder['orderId']))
    orderId = orderId[:-3]
    readCondition = "orderId IN ({})".format(orderId)

    #Consulta os chamados o bigquery de acordo com os pedidos da vtex
    bqOrders = read(readCondition)

    for bqOrder in bqOrders:
        #essa linha filtra e cria uma lista com apenas 1 item, aquele que corresponde ao orderId do bigquery
        vtexOrder = list(filter(lambda x:x["orderId"]==str(bqOrder.orderId),vtexOrders))
        status = str(vtexOrder[0]['status'])
        if (bqOrder.status != status):
            test = str(status) in orderUpadateList
            if (test == False):
                #cria a chave dentro do json
                orderUpadateList[status] = [bqOrder.orderId]
                #cria lista de status
                statusList.append(status)
            else:
                #adiciona orderId na chave criada acima
                orderUpadateList[status].append(bqOrder.orderId)

    for status in statusList:
        updateCondition = "orderId IN ({})".format(str(orderUpadateList[status])[1:-1])
        update("status = '" + status + "'", updateCondition)
    
    log.infoLog(str(datetime.today()) + " -- " + str(len(orderUpadateList)) + " status updated in %s seconds" % (time.time() - start_time))

    return







    #Carrega os pedidos em formato de OBJETO JSON para serem inseridos através do insertOrders()
# def loadJsonObj(orders):
#     for order in orders:
#         insertOrders(order.orderId , order.creationDate , order.status , order.totalValue , order.paymentNames)
#     return