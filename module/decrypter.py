from cryptography.fernet import Fernet

def decryptJson(jsonPath , keyPath):
    with open( jsonPath ,'rb') as f:
        jsonFile = f.read()

    with open(keyPath , 'rb') as file:
        key = file.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(jsonFile)
    decryptedJson = decrypted.decode('utf8')

    return decryptedJson