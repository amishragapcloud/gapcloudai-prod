import os
import openai
import streamlit as st
import pyodbc
import pandas as pd

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Azure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY_gpt_4")
openai.api_base = os.getenv("OPENAI_API_BASE_gpt_4")
openai.api_version = "2024-02-15-preview"
openai.api_type = "azure"  # Specify Azure OpenAI API type

# Replace 'your_deployment_id' with the actual deployment ID of your Azure OpenAI deployment
deployment_id = "sqlmodel"
connection_string = os.getenv("DB_CONNECTION_STRING")

# Set page config and add logo
st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)

def create_connection():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("Connection to Azure SQL Database successful!")
        return conn, cursor
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query_database(query, conn, cursor):
    """ Run SQL query and return results in a dataframe """
    df = pd.read_sql_query(query, conn)
    return df

def get_call_records():
    """ Get the values from the CallRecords table """
    conn, cursor = create_connection()
    if conn is not None:
        query = "SELECT PhoneNumber, CallTranscription FROM CallRecords"  # Modify this query as needed
        df = query_database(query, conn, cursor)
        close_connection(conn, cursor)
        return df
    else:
        return pd.DataFrame()

def summarize_paragraph(paragraph):
    system_message = "Summarize the following paragraph:"
    return get_text_from_messages(system_message, paragraph)

def get_text_from_messages(system_message, user_message, deployment_id="sqlmodel", temperature=0, max_tokens=1000) -> str:
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = openai.ChatCompletion.create(
        deployment_id=deployment_id,  # Specify your Azure deployment ID here
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return response.choices[0].message["content"]

def analyze_sentiment(text):
    system_message = "Analyze the sentiment of the following text:"
    return get_text_from_messages(system_message, text)

def suggest_next_action(text):
    system_message = "Suggest the next action based on the following text:"
    return get_text_from_messages(system_message, text)



logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Actions on your Data</h3>', 
            unsafe_allow_html=True)

st.markdown("      ") 

# Fetch call records and display in a DataFrame
call_records = get_call_records()


# Selectbox for choosing a phone number
selected_number = st.selectbox("Select Latest Caller", call_records["PhoneNumber"].tolist())

# Display associated transcription if a number is selected
if selected_number:
    transcription = call_records.loc[call_records["PhoneNumber"] == selected_number, "CallTranscription"].iloc[0]
    st.write("Call Transcription:")
    st.write(transcription)

    # Summarize the transcription
    summary = summarize_paragraph(transcription)
    if summary:
        st.subheader("Summary:")
        st.write(summary)

        # Analyze sentiment
        sentiment = analyze_sentiment(summary)
        if sentiment:
            st.subheader("Sentiment Analysis:")
            st.write(sentiment)

            # Suggest next action
            next_action = suggest_next_action(summary)
            if next_action:
                st.subheader("Next Action Items for the Caller:")
                st.write(next_action)

import os
import openai
import streamlit as st
import pyodbc
import pandas as pd

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Azure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY_gpt_4")
openai.api_base = os.getenv("OPENAI_API_BASE_gpt_4")
openai.api_version = "2024-02-15-preview"
openai.api_type = "azure"  # Specify Azure OpenAI API type

# Replace 'your_deployment_id' with the actual deployment ID of your Azure OpenAI deployment
deployment_id = "sqlmodel"
connection_string = os.getenv("DB_CONNECTION_STRING")

def create_connection():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("Connection to Azure SQL Database successful!")
        return conn, cursor
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query_database(query, conn, cursor):
    """ Run SQL query and return results in a dataframe """
    df = pd.read_sql_query(query, conn)
    return df

def get_call_records():
    """ Get the values from the CallRecords table """
    conn, cursor = create_connection()
    if conn is not None:
        query = "SELECT PhoneNumber, CallTranscription FROM CallRecords"  # Modify this query as needed
        df = query_database(query, conn, cursor)
        close_connection(conn, cursor)
        return df
    else:
        return pd.DataFrame()

def summarize_paragraph(paragraph):
    system_message = "Summarize the following paragraph:"
    return get_text_from_messages(system_message, paragraph)

def get_text_from_messages(system_message, user_message, deployment_id="sqlmodel", temperature=0, max_tokens=1000) -> str:
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = openai.ChatCompletion.create(
        deployment_id=deployment_id,  # Specify your Azure deployment ID here
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return response.choices[0].message["content"]

def analyze_sentiment(text):
    system_message = "Analyze the sentiment of the following text:"
    return get_text_from_messages(system_message, text)

def suggest_next_action(text):
    system_message = "Suggest the next action based on the following text:"
    return get_text_from_messages(system_message, text)


# Streamlit app
def main():
    col1, col2, col3 = st.columns([1, 1, 1])  # Divide the screen into two columns

    # Button for saving/download
    with col1:
        save_button = st.button("💾 Save to Database")

    # Button for feedback
    with col2:
        feedback_button = st.button("💌 Survey To Caller")

    # Button for feedback
    with col3:
        feedback_button = st.button("📥 Download Summary")

    # Handle button clicks
    if save_button:
        # Handle saving/download logic here
        pass
    elif feedback_button:
        # Handle feedback logic here
        pass


if __name__ == "__main__":
    main()
