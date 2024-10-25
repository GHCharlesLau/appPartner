# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:36:34 2024

Condition 2: Readreceipt & Prompt Response

@author: liuyu
"""

import streamlit as st
from openai import OpenAI
import numpy as np
import random, time
from datetime import datetime, timedelta


# Streamed response emulator (generator function)
def response_generator():
    response = "对话结束，请返回继续作答问卷。"
    for word in response.split():
        yield word + " "  # yield: produce a series of values over time, rather than computing them at once and sending them back like a list.
        time.sleep(0.001)

#%% Build a ChatGPT-like chatbots

st.title("Honey >_< ")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key= st.secrets["OPENAI_API_KEY2"],  # Free version: f200 requests/IP/Key/Day; KEY2: Paid version
    # base_url = "https://api.chatanywhere.tech/v1"  # domestic
    base_url = "https://api.chatanywhere.org/v1"  # overseas
    )


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"  # gpt-3.5-turbo, dall-e-2, dall-e-3

# Initialize chat history
# Use session state to store the chat history so we can display it in the chat message container.
if "messages" not in st.session_state:  # added a check to see if the messages key is in st.session_state. If it's not, we initialize it to an empty list. 
    st.session_state.messages = []
    # Add a system prompt to personalize the chatbot
    st.session_state.messages.append(
        {"role": "system", "content": "Your name is Li. You speak Chinese. You are a fictional romantic partner and you are going to plan a travelling plan with me. Your tone should not be that polite or passionate. Your sentences should not exceed three."}
        )


# Display chat messages from history on app rerun (eliminate the system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])


delayT = random.randint(1, 3)  # randomize deplayed time interval

# Accept user input and React to the user
if prompt := st.chat_input("在干啥？"):  # We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line.
    # Time display at first
    nowT = datetime.now().strftime("%H:%M:%S")  # Get current time
    st.write(f"<p style='backgroud-color:gray; text-align:center; font-size:10px'> {nowT} </p>", unsafe_allow_html=True)  # Display current time

    # Display user message in chat message container
    with st.chat_message("user", avatar=":material/account_circle:"):
        st.markdown(prompt)
     
    col1, col2 = st.columns([3,1])  # split the container into two columns
    with col2:
        with st.status("消息发送中...", expanded=True) as status:
            time.sleep(1)
            status.update(label="消息已送达", state="complete", expanded=True)
            time.sleep(2)
            status.update(label="已读 :white_check_mark:", state="complete", expanded=False)  # Set the readreceipt
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": ":material/account_circle:"})  # Add user message to chat history
    
    time.sleep(delayT)  # waiting for response
    nowT = datetime.now().strftime("%H:%M:%S")  # Get current time
    st.write(f"<p style='backgroud-color:gray; text-align:center; font-size:10px'> {nowT} </p>", unsafe_allow_html=True)  # Display current time
    
    # Display assistant response in chat message container
    if len(st.session_state.messages) < 20:  # Allow at most 10-turn conversation
        with st.chat_message("assistant", avatar=":material/face:"):
            stream = client.chat.completions.create(
                model = st.session_state["openai_model"],
                # Comprehension
                messages = [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ],
                stream = True,
            )
            response = st.write_stream(stream)  # Response
    else:
        with st.chat_message("assistant", avatar=":material/face:"):
            response = st.write_stream(response_generator())  # When exceeding conversation turns
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": ":material/face:"})

    
    
