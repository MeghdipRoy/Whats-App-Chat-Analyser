from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import emoji


extract = URLExtract()

def fetch_stats(selected_user, df):


#Count words
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]

    #fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]


    #fetch the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'count':'Percentages','user':'Names'})
    df = df[df['Names'] != 'Notification']
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    return x,df


def remove_urls(text):
    # Regex pattern to identify URLs
    url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')
def create_wordcloud(selected_user,df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words_hinglish = f.read().splitlines()
    with open('stopwords-bn.txt', 'r', encoding='utf-8') as b:
        stop_words_bn = b.read().splitlines()
    stop_words = list(set(stop_words_hinglish + stop_words_bn))


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[~df['user'].str.contains('Notification', na=False)]
    df = df[~df['message'].str.contains('<Media omitted>\n', na=False)]

    df['message'] = df['message'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    df['message'] = df['message'].apply(lambda x: remove_urls(remove_emojis(x)))

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

#remove emojies

def most_common_words(selected_user,df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words_hinglish = f.read().splitlines()
    with open('stopwords-bn.txt', 'r', encoding='utf-8') as b:
        stop_words_bn = b.read().splitlines()
    stop_words = stop_words_hinglish + stop_words_bn
    stop_words = list(set(stop_words))
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        message = remove_emojis(message)
        message = remove_urls(message)

        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns = {'0':'Word','1':'Count'})
    most_common_df.reset_index(drop=True, inplace=True)
    most_common_df.index += 1
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeLine(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    monthly_timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + "-" + str(monthly_timeline['year'][i]))

    monthly_timeline['time'] = time
    return monthly_timeline

def daily_timeLine(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap