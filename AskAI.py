import json
import streamlit as st
import pandas as pd
import sql_azdb
from prompts.prompts import SYSTEM_MESSAGE
from prompts.text_prompt import RESULT_MESSAGE
from prompts.bi import BI_MESSAGE
from openai_prompt.sql_openai import get_completion_from_messages
from openai_prompt.text_openai import get_text_from_messages
from openai_prompt.bi_openai import get_mataplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import ast
import dash
from dash import dcc, html
import importlib
import sys
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
from streamlit_lottie import st_lottie
import json 
import requests




st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)




# Add your logo image URL here
logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"

# HTML and CSS code for the logo
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""

# Add the logo HTML code to your Streamlit app
st.markdown(logo_html, unsafe_allow_html=True)




import streamlit as st

# Define the CSS style for the title
st.markdown(
    """
    <style>
    .title {
        
        
        text-decoration-color:  pink;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title at the top of the page
st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Conversations with your Data</h3>', 
            unsafe_allow_html=True)





# Initialize chatbot visibility state
if 'chatbot_visible' not in st.session_state:
    st.session_state['chatbot_visible'] = False

# Custom CSS for the button
button_css = """
    .custom-button {
        background-color: red;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
    }
    .custom-button:hover {
        opacity: 0.8;
    }
    .icon {
        vertical-align: middle;
    }
"""

# Add custom CSS to the page
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

# Button text with a robot icon
button_text = "Smart Assist 🤖"

if st.button(button_text, key="smart-assist-button"):
    st.session_state['chatbot_visible'] = not st.session_state['chatbot_visible']


# JavaScript code for toggling chatbot visibility
javascript_code = """
<script>
function toggleChatbot() {
    var chatbotPopup = document.getElementById("chatbot-popup");
    if (chatbotPopup.style.display === "none" || chatbotPopup.style.display === "") {
        chatbotPopup.style.display = "block";
    } else {
        chatbotPopup.style.display = "none";
    }
}
</script>
"""

html_code = f"""
{javascript_code}
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; position: relative;">
<div id="container" style="position: relative;">
    <div id="chatbot-popup" style="display: {'block' if st.session_state['chatbot_visible'] else 'none'}; position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
        <iframe src="https://copilotstudio.microsoft.com/environments/5e90b9ce-81ff-ee66-9e00-07f4cd1db1d7/bots/cr61d_broadMini/webchat?__version__=2" 
        frameborder="0" style="width: 400px; height: 500px;"></iframe>
    </div>
    <button onclick="toggleChatbot()" style="position: fixed; bottom: 20px; right: 20px; z-index: 1001;"></button>
</div>
</body>
</html>
"""

# Render the HTML code with toggle button and chatbot popup
st.markdown(html_code, unsafe_allow_html=True)





schemas = None
alerts = []
MAX_ALERTS = 5

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize session state variables
if 'alerts' not in st.session_state:
    st.session_state['alerts'] = []

def create_alert():
    # Adding a new alert to the list
    if len(st.session_state['alerts']) < MAX_ALERTS:
        alert = {
            'table': selected_table,
            'column': selected_column,
            'condition': condition,
            'value': value
        }
        st.session_state['alerts'].append(alert)
        st.success("Alert created successfully!")
    else:
        st.error(f"You can only create up to {MAX_ALERTS} alerts.")

def delete_alert(index):
    # Function to delete an alert
    st.session_state['alerts'].pop(index)
    st.experimental_rerun()

import datetime
import json
import requests

def access_token(azure_key, azure_client_id):
    password = azure_key
    grant_type = "client_credentials"
    scope = "https://graph.microsoft.com/.default"
    data = {
        "client_id": azure_client_id,
        "client_secret": password,
        "grant_type": grant_type,
        "scope": scope
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}
    auth_url = "https://login.microsoftonline.com/a732e66b-3be9-40c9-aa6c-8a56966a170d/oauth2/v2.0/token"
    response = requests.post(auth_url, data=data, headers=headers)

    responseObject = json.loads(response.text)

    return responseObject['access_token']

class EmailAddress:
    def __init__(self, address):
        self.address = address

class Recipient:
    def __init__(self, email_address):
        self.emailAddress = email_address

class EmailBody:
    def __init__(self, content_type, content):
        self.contentType = content_type
        self.content = content

class EmailMessage:
    def __init__(self, subject, body, to_recipients, cc_recipients):
        self.subject = subject
        self.body = body
        self.toRecipients = to_recipients
        self.ccRecipients = cc_recipients

class EmailPayload:
    def __init__(self, message, save_to_sent_items):
        self.message = message
        self.saveToSentItems = save_to_sent_items

def generate_email_payload(mail_message_dto):
    recipients_list = [Recipient(EmailAddress(recipient)) for recipient in mail_message_dto['receiver_emails']]
    email_message = EmailMessage(
        subject=mail_message_dto['subject'],
        body=EmailBody(content_type="Text" if not mail_message_dto['body_type'] else mail_message_dto['body_type'],
                       content="No Message" if not mail_message_dto['body'] else mail_message_dto['body']),
        to_recipients=recipients_list,
        cc_recipients=[]
    )
    email_payload = EmailPayload(message=email_message, save_to_sent_items=str(mail_message_dto['save_to_sentItem']))
    return json.dumps(email_payload, default=lambda o: o.__dict__, indent=4)

def send_message(mail_message_dto):
    access_token_result = access_token("sLJ8Q~RIUGBm6Gn1CUMFlhWerQfBgXtTvGxGZaSk", "c7ccd920-54be-4d38-bc70-3c65bdf016fb")
    json_payload = generate_email_payload(mail_message_dto)
    url_base = f"https://graph.microsoft.com/v1.0/users/noreply@gapcloud.com.au/sendMail"
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {access_token_result}"
    }
    response = requests.post(url_base, headers=headers, data=json_payload)

    if not response.ok:
        if "INVALID_OAUTH" in response.text:
            pass  # Handle INVALID_OAUTH condition if necessary
        raise print(response.text)

    return response.text

def send_email():
    if email_address and st.session_state['alerts']:
        mail_message_dto = {
            "receiver_emails": [email_address],
            "subject": "Alert Notification",
            "body": "\n".join([f"{alert['table']} {alert['column']} {alert['condition']} {alert['value']}" for alert in st.session_state['alerts']]),
            "body_type": "Text",
            "sender_email": "noreply@gapcloud.com.au",
            "save_to_sentItem": False
        }
        try:
            response = send_message(mail_message_dto)
            st.success("Email notification sent successfully!")
        except Exception as e:
            st.error(f"Error sending email: {e}")
    else:
        st.warning("Please enter your email address and create alerts before sending notifications.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to clear chat messages
def clear_chat():
    st.session_state.messages = []

# Add "New Chat" button in the sidebar
if st.sidebar.button("New Chat 💬"):
    clear_chat()
    st.experimental_rerun()

# Schema Retrieval
schemas = sql_azdb.get_schema_representation()
print(schemas)  # Add this line to print the retrieved schema information
  
        




def get_formatted_db_schema(formatted_db_schema, prompt, previous_response=None):
    """
    Function to get the formatted database schema and SQL query response.
    If an error occurs, it resends the prompt with the previous response and error.
    """
    try:
        response = get_completion_from_messages(formatted_db_schema, prompt)
        sql_response_lines = response.split('\n')
        code_lines = [line for line in sql_response_lines if line != '```json' and line != '```']
        formatted_sql_response = '\n'.join(code_lines)
        json_response = json.loads(formatted_sql_response)
        query = json_response['query']
        return query
    except Exception as e:
        if previous_response:
            error_message = formatted_db_schema + str(e) + "\n" + previous_response
            response = get_completion_from_messages(error_message, prompt)
            return get_formatted_db_schema(response, prompt, response)
        else:
            print(f"Error: {e}")
            return None





def execute_sql_query(query, conn, cursor):
    """
    Function to execute the SQL query and handle the results.
    """
    try:
        sql_results = sql_azdb.query_database(query, conn, cursor)
        return sql_results
    except Exception as e:
        print(f"SQL Error: {e}")
        return None

def generate_iframe():
    return """
    <iframe title="Insights_BI_Reports" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=d7faa383-69e8-4448-be7c-642953ffec78&autoAuth=true&ctid=a732e66b-3be9-40c9-aa6c-8a56966a170d" frameborder="0" allowFullScreen="true"></iframe>
    """


from streamlit import components

def handle_sql_results(st, query, sql_results):
    response_content = ""
    if len(sql_results) < 6:
        prompt_formatted_message = RESULT_MESSAGE.format(prompt=query)
        text_response = get_text_from_messages(query, sql_results)
        response_content += text_response + "\n"
        st.write(text_response)
        st.dataframe(sql_results)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
    else:
        data = sql_results.values.tolist()
        bi_formatted_message = BI_MESSAGE.format(prompt=query)
        bi_response = get_mataplotlib(bi_formatted_message, data)
        formatted_bi_response = format_bi_response(bi_response)
        execute_bi_code(st, formatted_bi_response, data, sql_results)
        dashboard_url = "https://app.powerbi.com/reportEmbed?reportId=d7faa383-69e8-4448-be7c-642953ffec78&autoAuth=true&ctid=a732e66b-3be9-40c9-aa6c-8a56966a170d"
        iframe_code = f'<iframe src="{dashboard_url}" width="900" height="500.25" frameborder="0" allowFullScreen="true"></iframe>'
        response_content += f"{iframe_code}\n"
        st.markdown("Replated BI Report:")
        st.markdown(iframe_code, unsafe_allow_html=True) 

    return response_content





def format_bi_response(bi_response):
    """
    Function to format the BI response by removing the code block markers.
    """
    bi_response_lines = bi_response.split('\n')
    code_lines = [line for line in bi_response_lines if line != '```python' and line != '```']
    formatted_bi_response = '\n'.join(code_lines)
    print(formatted_bi_response)
    return formatted_bi_response

def execute_bi_code(st,formatted_bi_response, data, sql_results):
    """
    Function to execute the generated BI code and handle any errors.
    If an error occurs, it resends the prompt with the previous response and error.
    """
    locals = {}

    # Parse the generated code to extract import statements
    try:
        parsed_code = ast.parse(formatted_bi_response)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return

    # Dynamically import required modules
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.Import):
            for alias in node.names:
                try:
                    importlib.import_module(alias.name)
                except ImportError as e:
                    print(f"Import Error: {e}")
        elif isinstance(node, ast.ImportFrom):
            try:
                imported_module = importlib.import_module(node.module)
                for alias in node.names:
                    full_name = f"{node.module}.{alias.name}"
                    try:
                        imported_submodule = importlib.import_module(full_name)
                        setattr(locals, alias.name, getattr(imported_submodule, alias.name))
                    except ImportError:
                        try:
                            setattr(locals, alias.name, getattr(imported_module, alias.name))
                        except AttributeError:
                            try:
                                locals[alias.name] = importlib.import_module(full_name)
                            except ImportError as e:
                                print(f"Import Error: {e}")
            except ImportError as e:
                print(f"Import Error: {e}")

    try:
        exec(formatted_bi_response, globals(), locals)
    except Exception as e:
        print(f"Code Error: {e}")
        error_message = f"Error: {str(e)}\n\nOriginal Code:\n{formatted_bi_response}"
        bi_response = get_mataplotlib(error_message, data)
        execute_bi_code(st,bi_response, data, sql_results)
    else:
        generated_fig_func = locals['generate_fig']
        fig = generated_fig_func()
        st.dataframe(sql_results)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, height=400)






        
def main():
    global schemas  # Use the global schemas variable
    if formatted_db_schema and prompt:
        query = get_formatted_db_schema(formatted_db_schema, prompt)
        if query:
            sql_results = execute_sql_query(query, conn, cursor)
            if sql_results is not None:
                handle_sql_results(st,prompt, sql_results)


conn_tuple = sql_azdb.create_connection()
conn = conn_tuple[0]  # Extracting the connection object from the tuple
cursor = conn_tuple[1]
    





def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
       
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("");
          background-size: 200px 200px;
  background-repeat: no-repeat; 
background-position: right top;        }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()





# Custom CSS styles
custom_css = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        
    }
    .container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-top: 50px;
    }
    .user-input {
        margin-bottom: 20px;
    }
    .generated-query {
        margin-top: 30px;
    }
    .error-message {
        color: #FF0000;
    }
</style>
"""



# Display custom CSS
st.markdown(custom_css, unsafe_allow_html=True)


st.markdown("")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

formatted_db_schema = ""  # Define a default value for formatted_db_schema

user_questions = st.session_state.get("user_questions", [])

if prompt := st.chat_input("What Insights Do You Need?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    if prompt and schemas is not None:
        formatted_db_schema = SYSTEM_MESSAGE + f"\nHere is the schema of the table: {schemas}"
    elif not schemas:
        st.error("Ah! Could Not Connect Now.")

    with st.chat_message("user"):
        st.markdown(prompt)


        user_questions.append(prompt)
        st.session_state.user_questions = user_questions  # Update session state

    # Display all captured questions in the sidebar
    st.sidebar.title("Asked Questions:")
    for idx, question in enumerate(user_questions, start=1):
        st.sidebar.write(f"Question {idx}: {question}")




    main()






import streamlit as st

def handle_conversation_starter(st, query):
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        formatted_db_schema = ""  # Define a default value for formatted_db_schema

        if query == "Show me the Avg ACW Time last week.":
            # Define SQL query to retrieve average ACW time from your database
            sql_query = "SELECT AVG(ACW_Time) AS Avg_ACW_Time FROM service_in_time_counters;"
            sql_results = execute_sql_query(sql_query, conn, cursor)
            if sql_results is not None and not sql_results.empty:  # Check if sql_results is not None and not empty
                handle_sql_results(st, sql_query, sql_results)
                st.markdown('<span>The average ACW (After Call Work) time is 2 seconds.</span><span>🕒</span>', unsafe_allow_html=True)
            else:
                st.error("Error executing SQL query or empty result.")

        elif query == "Show me the Avg ACW Time by Service Name.":
            # Define SQL query to retrieve average ACW time by service name from your database
            sql_query = "SELECT Service_Name, AVG(ACW_Time) AS Avg_ACW_Time FROM service_in_time_counters GROUP BY Service_Name;"
            sql_results = execute_sql_query(sql_query, conn, cursor)
            if sql_results is not None and not sql_results.empty:  # Check if sql_results is not None and not empty
                handle_sql_results(st, sql_query, sql_results)
                st.markdown('<span>The average ACW (After Call Work) time by Service Name is as follows.</span><span>📊</span>', unsafe_allow_html=True)
            else:
                st.error("Error executing SQL query or empty result.")

        elif query == "Show me the Avg ACW Time":
            # Define SQL query to retrieve average ACW time by team name from your database
            sql_query = "SELECT AVG(ACW_Time) AS Avg_ACW_Time FROM service_in_time_counters;"
            sql_results = execute_sql_query(sql_query, conn, cursor)
            if sql_results is not None and not sql_results.empty:  # Check if sql_results is not None and not empty
                handle_sql_results(st, sql_query, sql_results)
                st.markdown('<span>The average ACW (After Call Work) time is as follows.</span><span>⏱️</span>', unsafe_allow_html=True)
            else:
                st.error("Error executing SQL query or empty result.")

        else:
            st.error("Invalid conversation starter.")

    else:
        st.error("Empty query.")






# Add conversation starters as buttons
if not st.session_state.messages:
        # Add conversation starters as buttons and text
        st.markdown('<div style="text-align: center; color: orange;">Don\'t know where to start?</div><div style="text-align: center; color: green;"> Try These.....</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("📊 Show me the Avg ACW Time during last week."):
                handle_conversation_starter(st,"Show me the Avg ACW Time last week.")
        with col2:
            if st.button("📈 Show me the Avg ACW Time by Service Name."):
                handle_conversation_starter(st,"Show me the Avg ACW Time by Service Name.")
        with col3:
            if st.button("📉 Show me the Avg ACW Time by Team Name."):
                handle_conversation_starter(st,"Show me the Avg ACW Time by Team Name")

        st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import asyncio  # Added asyncio import
import requests
import json
from dataclasses import dataclass
from typing import List

def access_token(azureKey, azureClientId):
    password = azureKey
    grant_type = "client_credentials"
    scope = "https://graph.microsoft.com/.default"
    data = {
        "client_id": azureClientId,
        "client_secret": password,
        "grant_type": grant_type,
        "scope": scope
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}
    auth_url = "https://login.microsoftonline.com/a732e66b-3be9-40c9-aa6c-8a56966a170d/oauth2/v2.0/token"
    response = requests.post(auth_url, data=data, headers=headers)
    responseObject = json.loads(response.text)
    return responseObject['access_token']

class EmailAddress:
    def __init__(self, address):
        self.address = address

class Recipient:
    def __init__(self, email_address):
        self.emailAddress = email_address

class EmailBody:
    def __init__(self, content_type, content):
        self.contentType = content_type
        self.content = content

class EmailMessage:
    def __init__(self, subject, body, to_recipients, cc_recipients):
        self.subject = subject
        self.body = body
        self.toRecipients = to_recipients
        self.ccRecipients = cc_recipients

class EmailPayload:
    def __init__(self, message, save_to_sent_items):
        self.message = message
        self.saveToSentItems = save_to_sent_items

def generate_email_payload(mail_message_dto):
    recipients_list = [Recipient(EmailAddress(recipient)) for recipient in mail_message_dto['receiver_emails']]
    email_message = EmailMessage(
        subject=mail_message_dto['subject'],
        body=EmailBody(content_type="Text" if not mail_message_dto['body_type'] else mail_message_dto['body_type'],
                       content="No Message" if not mail_message_dto['body'] else mail_message_dto['body']),
        to_recipients=recipients_list,
        cc_recipients=[]
    )
    email_payload = EmailPayload(message=email_message, save_to_sent_items=str(mail_message_dto['save_to_sentItem']))
    return json.dumps(email_payload, default=lambda o: o.__dict__, indent=4)

def send_message(mail_message):
    access_token_result = access_token("sLJ8Q~RIUGBm6Gn1CUMFlhWerQfBgXtTvGxGZaSk", "c7ccd920-54be-4d38-bc70-3c65bdf016fb")
    json_payload = generate_email_payload(mail_message)
    url_base = f"https://graph.microsoft.com/v1.0/users/{mail_message['sender_email']}/sendMail"
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {access_token_result}"
    }
    response = requests.post(url_base, headers=headers, data=json_payload)

    if not response.ok:
        if "INVALID_OAUTH" in response.text:
            pass  # Handle INVALID_OAUTH condition if necessary
        raise print(response.text)

    return response.text

async def main():
   if st.session_state.messages:
        # Add a button to send email only if a response has been generated
        if st.button("📧"):
            # Get the last generated response from session_state
            last_response = st.session_state.messages[-1]["content"]

            mail_message_dto = {
                "receiver_emails": ["amishra@gapcloud.com.au"],
                "subject": "Generated Response",
                "body": last_response,
                "body_type": "Text",
                "sender_email": "noreply@gapcloud.com.au",
                "save_to_sentItem": True  # or False based on your requirement
            }

            response = send_message(mail_message_dto)
            st.write(response)  # Show response from sending email
        


asyncio.run(main())


if __name__ == "__main__":


    # Schema Representation
    schemas = sql_azdb.get_schema_representation()
    print(schemas)

    main()
