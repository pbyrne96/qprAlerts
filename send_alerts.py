from datetime import datetime
import json
from twilio.rest import Client
from dotenv import load_dotenv;load_dotenv()
import os
from send_email import sendgrid_send

class send_alert:

    def __init__(self,filename: str ) -> None:
        self.client = Client(os.getenv('account_sid'),os.getenv('twillio_auth'))
        self.source_file = filename
        self.time_frame_dd = [0,1]
        self.data_fmt = "%d/%m/%Y:%H:%M"
        self.apply_dt = lambda x: datetime.strptime(x,self.data_fmt)
        self.sf_as_dict = self.open_source_file()
        self.twillio_no = os.getenv('twillio_no')
        self.days_to=None
        self.msg = None

    def open_source_file(self,source_file=None) -> dict[str,str]:
        if not(source_file):
            source_file = self.source_file
        with open(source_file) as f:
            return json.load(f)

    def get_nearest_game(self) -> datetime:
        dates = [*map(self.apply_dt,self.sf_as_dict.keys())]
        dates.sort()
        return dates[0]

    def check_time_to_game(self) -> int:
        nearest_game = self.get_nearest_game()
        now = datetime.strptime(datetime.now().strftime(self.data_fmt),self.data_fmt)
        return (nearest_game-now).days,now,nearest_game
       
    def remove_date_passed(self,key_to_remove:datetime):
        self.sf_as_dict.pop(key_to_remove.strftime(self.data_fmt))
        with open(self.source_file,'w') as f:
            json.dump(self.sf_as_dict,f,indent=1)

    def set_msg(self,days:int):
        if days==0:
            return "QPR game is today "
        return """Warning: QPR Game in {} day(s)""".format(days)

    def send_whatsapp_alert(self)-> None:
        numbers = os.getenv('numbers').split(',') # --> change to get numbers method in time
        [*map(self.send_wsp_twlo,numbers)]
    
    def send_wsp_twlo(self,number:str) -> None:
        
        message_send = self.client.messages.create(
            from_=f'whatsapp:+{self.twillio_no}',
            body=self.msg,
            to=f'whatsapp:{number}'
        )
        return message_send.sid

    def send_email(self,from_:str) -> None:
        # -->> will connect with the sendgridd API on send_email.py 
        to = tuple(os.getenv('emails').split(','))
        status = sendgrid_send(self.msg,from_,to)
        return status
            
        
    def __main__(self):
        nearest_game_dd,now,n_g_full_date = self.check_time_to_game()
        self.days_to = nearest_game_dd
        self.msg = self.set_msg(self.days_to)
        if(nearest_game_dd in self.time_frame_dd):
            print('activate')
            self.send_whatsapp_alert()
            self.remove_date_passed(n_g_full_date)
            check = self.send_email(os.getenv('senderEmail'))
        return nearest_game_dd
        

if __name__ == "__main__":
    cls = send_alert('home_fixtures.json').__main__()
    print(cls)