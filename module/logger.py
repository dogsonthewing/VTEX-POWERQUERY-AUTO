import logging

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)

def debugLog(log):
    logging.debug(log)
    return

def infoLog(log):
    logging.info(log)
    return

def warningLog(log):
    logging.warning(log)
    return

def errorLog(log):
    logging.debug(log)
    return