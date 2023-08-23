import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import time

from model import *
from data import  *

# Set API Key ----------------------------------------------------------------
import os
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['ZAPIER_NLA_API_KEY'] = st.secrets['ZAPIER_NLA_API_KEY']

# Set session state
def clear_submit():
    st.session_state["submit"] = False

st.set_page_config(page_title="HireBrighter - An LLM-powered hiring assistant", page_icon=":star:", layout='wide')
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("HireBrighter - Understand your Resume Database")

# Sidebar contents
with st.sidebar:
    st.title(':star: HireBrighter')
    st.markdown('''
    ## About
    This app is an LLM-powered hiring assistant built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/en/latest/)
    
    ''')

    add_vertical_space(5)
    st.write('Made by HYPE AI :book:')

# Layout of input/response containers ----------------------------------------------------------------
zapier_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()
context_container = st.container()
colored_header(label='', description='', color_name='blue-30')
process_button = st.button("Process")
stats_container = st.container()
chat_container = st.container()

# Zapier Button --------------------------------
with zapier_container:
    st.markdown('**Zapier** allows you to automate email generation, scheduling and more! Get your API key [here](https://nla.zapier.com/docs/authentication/#api-key)!')
    st.markdown('_Note: Your API key will be deleted immediately once the webpage is refreshed._')
    st.markdown('_Please specify the email address for any scheduling tasks._')
    st.session_state["zapier"] = False
    user_zapier_api_key = st.text_input('Your must enter your Zapier API Key to use the full functionalities', '')
    if user_zapier_api_key:
        os.environ['ZAPIER_NLA_API_KEY'] = user_zapier_api_key
        st.session_state["zapier"] = True

# User input ------------------------------------------------------------------
## Function for taking user provided PDF as input
def get_file(key):
    uploaded_files = st.file_uploader(f"Upload your {key}", type='pdf', key=key, on_change=clear_submit, accept_multiple_files=True)
    return uploaded_files

## Applying the user input box
with input_container:
    files = get_file('resumes')

# Process Button ------------------------------------------------------------------
def get_agent_from_data(files):
    # 1. Read and process data
    resumes = []
    for file in files:
        resumes.append(get_text_from_pdf(file))

    # 2. Build an agent from the database
    overall_chain, agent, df_database = get_agent(resumes, embedding_type='InstructXL', parse_method='one_shot')
    return overall_chain, agent, df_database

if process_button:
    st.session_state.messages = []

    if not files:
        st.error("Please upload at least one document!")
    else:
        with st.spinner('Processing... It will take a while...'):
            start_time = time.time()
            st.session_state["process_chain"], st.session_state["agent"], st.session_state["dataframe"] = get_agent_from_data(files)
            print(time.time() - start_time)

        st.success('Done!')
        st.session_state["submit"] = True

# Statistics ----------------------------------------------------------------
with stats_container:
    if st.session_state.get("submit"):
        if not st.session_state["dataframe"].empty:
            st.dataframe(st.session_state["dataframe"])

# Chatbot GUI ----------------------------------------------------------------
with chat_container:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.get("submit"):
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me anything about the resumes!"):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                agent = st.session_state["agent"]
                process_chain = st.session_state["process_chain"]

                processed_prompt = process_chain({'prompt': prompt})['answer']
                full_response = agent.run(prompt)

                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
