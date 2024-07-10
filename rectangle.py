from urlextract import URLExtract
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import pandas as pd
from collections import Counter
import emoji
import re

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
        #no of words
    words=[]
    for message in df['message']:
            words.extend(message.split())
    #no of media
    num_media_messages = df[df['message'].str.contains('<Media omitted>', case=False)].shape[0]
   #links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages ,len(words),num_media_messages,len(links)
def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def word_cloud_rep(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        temp = df[df['user'] != 'group notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
    else:
        temp = df[df['user'] != 'group notification']
        temp = temp[temp['message'] != '<Media omitted>\n']

    stop_words = set(stopwords.words('english'))
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]


    emojis = []
    for message in df['message']:
        emojis.extend(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]', message))
    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
 

    
    
def monthly_timeline(selected_user, df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = [f"{month}-{year}" for year, month in zip(timeline['year'], timeline['month'])]
    timeline['time'] = time

    return timeline


def word_cloud_rep(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
    
def most_common_words(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
        temp = df[df['user'] != 'group notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
    else:
        temp = df[df['user'] != 'group notification']
        temp = temp[temp['message'] != '<Media omitted>\n']

    stop_words = set(stopwords.words('english'))
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def daily_timeline(selected_user, df):
    # Filter the DataFrame based on the selected user
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    # Check if the DataFrame is not empty after filtering
    if df.empty:
        return pd.DataFrame(columns=['only_date', 'message_count'])

    # Group by 'only_date' and count the number of messages for each date
    daily_timeline = df.groupby('only_date').size().reset_index(name='message_count')

    return daily_timeline

    
