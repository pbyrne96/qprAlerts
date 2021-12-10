import os 
import re
import json
from datetime import datetime

class format_fixture_list:
    def __init__(self,filename: str ) -> None:
        self.filename = filename
        self.target_path = '/home_fixtures.json'
        self.search_pattern = re.compile(r'[a-z]',re.I)
        self.data_fmt = "%d/%m/%Y:%H:%M"
        self.working_dict = self.populate_working_dict()
        self.apply_dt = lambda x: datetime.strptime(x,self.data_fmt)
        self.dt_to_str = lambda x : x.strftime(self.data_fmt)

    
    def clean_line(self,s) -> str:
        return "".join(re.sub(r'[-]',':',s)).replace(' ','')[:-1]

    def submit_file_to_db(self, target_path=None):
        if not(target_path):
            target_path = self.target_path
        with open(os.path.join(os.getcwd())+target_path,'w') as f:
            json.dump(self.filter_past_dates(),f,indent=1)

    def populate_working_dict(self,filename=None) -> dict[str,str]:
        if filename in os.listdir():
            filename = self.filename
        
        with open(self.filename,'r') as f:
            timestamps,fixtures =[],[]
            for line in f.readlines():
                if line != '\n':
                    line = line.replace('\n','')
                    index = self.search_pattern.search(line).start()
                    fixture = line[index:]
                    
                    if(re.search(r"\(([h_]+)\)",fixture,re.I)):
                        timestamps.append(self.clean_line(line[:index])),fixtures.append(fixture)
            return {timestamps[i]:fixtures[i] for i in range(len(timestamps))}

    def filter_past_dates(self):
        future_games = []
        now = datetime.strptime(datetime.now().strftime(self.data_fmt),self.data_fmt)
        for date in list(map(self.apply_dt,[*self.working_dict.keys()])):
            t = future_games.append(date) if date > now else None
        return {date: self.working_dict.get(date) for date in [*map(self.dt_to_str,future_games)]}

    def __main__(self):
        self.submit_file_to_db()

if __name__ == "__main__":
    ffl = format_fixture_list('fixture_list.txt').__main__()
    
