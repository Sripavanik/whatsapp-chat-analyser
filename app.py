import streamlit as st
import preprocessor,rectangle
import matplotlib.pyplot as plt
st.sidebar.title("WhatsApp Chat Analyser")
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
        st.header("Total words")
        st.title(words) 
    with col3:
        st.header("Media messages")
        st.title(num_media_messages) 
    with col4:
        st.header("Links shared")
        st.title(num_links)
    #monthly timeline
    '''st.title('Monthly timeline')
    st.write(df)
    if selected_user=='Overall':
        timeline=rectangle.monthly_timeline(selected_user,df)
        
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)'''
    if selected_user=='Overall':
        st.title("Most busy users")
        col1,col2=st.columns(2)
        x,new_df=rectangle.most_busy_users(df)
        fig,ax=plt.subplots()
        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    st.title('Wordcloud')
    df_wc=rectangle.word_cloud_rep(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    #most common words
    most_common_df=rectangle.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most common words')
    st.pyplot(fig)
    emoji_df=rectangle.emoji_helper(selected_user,df)
    st.title('Emoji analysis')
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        # Assuming 'emoji_df' has columns in the order label, value
        ax.pie(emoji_df.iloc[:, 1], labels=emoji_df.iloc[:, 0], autopct="%0.2f")

    
        st.pyplot(fig)