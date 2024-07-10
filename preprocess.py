import pandas as pd
import re

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s'
    messages=re.split(pattern,data)[1:]
   
    dates=re.findall(pattern,data)
    editdate = [date.replace('\u202f', ' ') for date in dates]
    df=pd.DataFrame({'user_messages':messages,'editdate':editdate})
    users=[]
    messages=[]
    for message in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:#username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
        df['user']=users
        df['message']=messages
        df.drop(columns=['user_messages'],inplace=True)
        df['date'] = pd.to_datetime(df['editdate'].str.strip(), format='%m/%d/%y, %I:%M%p', errors='coerce')
        df['year']=df['date'].dt.year
        df['month']=df['date'].dt.month_name()
        df['day']=df['date'].dt.day
        df['hours']=df['date'].dt.hour
        df['mins']=df['date'].dt.minute
        return df