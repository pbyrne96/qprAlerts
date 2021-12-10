from dotenv import load_dotenv;load_dotenv()
import os
from sendgrid import SendGridAPIClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, MailSettings , BypassListManagement )
                                
                                
def sendgrid_send(msg,from_email,to_emails):
    """ sends important emails through sendgrid API with the capability of bypassing their 
        list management system for recipents who may have unsubcribed """
    sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))

    ex_message = Mail(
        from_email=from_email,
        to_emails=[to_emails],
        subject='QPR game is soon',
        html_content=msg)

  
    mail_settings = MailSettings()
    mail_settings.bypass_list_management = BypassListManagement(True)
    ex_message.mail_settings = mail_settings

    response = sendgrid_client.send(ex_message)
    status = response.status_code
    if status<400:
        return {
            'status': status,
            'body': ex_message.get()
        }
    else:
        raise RuntimeError(f" failed to send as the Status code is {status} ")