import smtplib
from modules.logger import errorLog

def sendEmail(message):
    try: 
        #Create your SMTP session 
        smtp = smtplib.SMTP('smtp.gmail.com', 587) 

    #Use TLS to add security 
        smtp.starttls() 

        #User Authentication 
        smtp.login("remetente@email.com.br","senha123")

        #Defining The Message 
        message = message 

        #Sending the Email
        smtp.sendmail("remetente@email.com.br", "destinatário@email.com.br",message)

        #Terminating the session 
        smtp.quit() 
        print ("Email sent successfully!") 

    except Exception as ex: 
        print("Something went wrong....",ex)
        errorLog('Falha ao enviar o e-mail')
    return