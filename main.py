import streamlit as st
import preprocessor,rectangle
import matplotlib.pyplot as plt
st.set_page_config(
    page_title="WhatsApp chat Analyser",
    page_icon="whatsApp.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Your Streamlit app content goes here

st.sidebar.title("WhatsApp chat Analyser")
upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    #fetch unique users
    
    user_list=df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        pass
    num_messages,words,num_media_messages,num_links=rectangle.fetch_stats(selected_user,df)
    st.title('top Statistics')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Media shared")
        st.title(num_media_messages)
    with col4:
        st.header("Links shared")
        st.title(num_links)
    st.title("Monthly timeline")
    
    timeline=rectangle.monthly_timeline(selected_user,df)
    
    fig,ax=plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color='green')
    st.pyplot(fig)
    st.title("Daily timeline")
    
    daily_timeline=rectangle.daily_timeline(selected_user,df)
   
    fig,ax=plt.subplots()
    
    ax.plot(daily_timeline['only_date'],daily_timeline['message_count'])
    
    st.pyplot(fig)
    st.title('Emoji analysis')
    col1, col2 = st.columns(2)
    with col1:
        emoji_df = rectangle.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)

    with col2:
        emoji_df = rectangle.emoji_helper(selected_user, df)
        fig, ax = plt.subplots()
    # Assuming 'emoji_df' has columns in the order label, value
        ax.pie(emoji_df.iloc[:, 1], labels=emoji_df.iloc[:, 0], autopct="%0.2f")

       
      
# Display the plot using Streamlit
    st.pyplot(fig)
    st.title('Wordcloud')
    df_wc=rectangle.word_cloud_rep(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    most_common_df=rectangle.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most common words')
    st.pyplot(fig)
    