import re
import pandas as pd

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[A-Za-z][A-Za-z]\s-\s"
    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['date1'] = pd.to_datetime(df['date'], format="%d/%m/%y, %I:%M %p - ")
    df['only_date'] = df['date1'].dt.date
    df['year'] = df['date1'].dt.year
    df['month'] = df['date1'].dt.strftime('%B')
    df['month_num'] = df['date1'].dt.month
    df['day'] = df['date1'].dt.day
    df['day_name'] = df['date1'].dt.day_name()
    df['hour'] = df['date1'].dt.strftime('%I').astype(int)
    df['minute'] = df['date1'].dt.minute
    df['am_pm'] = df['date1'].dt.strftime('%p')
    period = []
    for hour in df['hour']:
        if hour == 12:
            period.append(str(hour) + "-" + str(1) + " PM")
        elif hour == 0:
            period.append(str(12) + "-" + str(hour + 1) + " AM")
        elif 0 < hour < 12:
            period.append(str(hour) + "-" + str(hour + 1) + " AM")
        else:
            period.append(str(hour - 12) + "-" + str(hour - 11) + " PM")
    df['period'] = period
    df.drop(columns=['date1'], inplace=True)
    return df