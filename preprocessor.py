# preprocessor.py

import pandas as pd
import re

def preprocess(data):
    users = []  # Define 'users' list here
    messages = []
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
   
    df = pd.DataFrame({'user_messages': messages, 'date': dates})

    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    # Adjust lengths of 'users' and 'messages' to match the length of the DataFrame
    users = users[:len(df)]
    messages = messages[:len(df)]

    # Add columns to DataFrame
    df['user'] = users
    df['message'] = messages

    # Convert 'date' to datetime explicitly
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Check and print relevant information
    print("Length of DataFrame after date conversion:", len(df))
    print("Unique values in 'date' after conversion:", df['date'].unique())

    # Print rows with 'None' values in 'date'
    print("Rows with 'None' values in 'date':")
    print(df[df['date'].isnull()])

    # Extract date-related features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hours'] = df['date'].dt.hour
    df['mins'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date

    # Drop unnecessary columns
    df.drop(columns=['user_messages'], inplace=True)

    print("Length of DataFrame after feature extraction:", len(df))

    return df
