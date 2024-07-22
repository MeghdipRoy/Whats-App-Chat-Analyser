import pylab as pl
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzers")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    num_messages, words, num_media_messages, links  = helper.fetch_stats(selected_user,df)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div style="text-align: center;">
                    <span style="font-size: 1.5em;">Total Messages: </span>
                    <span style='font-size: 2em; color: #FF6347;'>{num_messages}</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="text-align: center;">
                    <span style="font-size: 1.5em;">Total Words: </span>
                    <span style='font-size: 2em; color: #FF6347;'>{words}</span>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                       <div style="text-align: center;">
                           <span style="font-size: 1.5em;">Media Shared: </span>
                           <span style='font-size: 2em; color: #FF6347;'>{num_media_messages }</span>
                       </div>
                       """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                       <div style="text-align: center;">
                           <span style="font-size: 1.5em;">Link Shared: </span>
                           <span style='font-size: 2em; color: #FF6347;'>{links}</span>
                       </div>
                       """, unsafe_allow_html=True)

        # monthly timeLine
        st.title("Monthly TimeLine")
        monthly_timeline = helper.monthly_timeLine(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily TimeLine")
        daily_timeline = helper.daily_timeLine(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map

        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.weekly_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group(Group leve)
        if selected_user == 'Overall':
            st.title('Most busy users')

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = pl.subplots()


        ax.barh(most_common_df[0], most_common_df[1])
        # plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        #emoji analysis

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)





