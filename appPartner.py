# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:36:34 2024

@author: liuyu
"""

import streamlit as st
from openai import OpenAI
import numpy as np
import random, time

#%% Build a ChatGPT-like chatbots

st.title("Honey >_<")

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
        {"role": "system", "content": "Your name is Li. You are a fictional romantic partner and you are going to plan a tour guidebook with me. Your tone should not be that optimistic and polite because we are intimate, and sentences should not exceed three."}
        )


# Display chat messages from history on app rerun (eliminate the system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# # wait several seconds to continue    
delayT = random.randint(5, 10)  # randomize deplayed time interval
    
# Accept user input and React to the user
if prompt := st.chat_input("What is up?"):  # We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line. 
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        with st.status("消息发送中...", expanded=True) as status:
            time.sleep(1)
            status.update(label="消息已送达", state="complete", expanded=True)
            time.sleep(delayT)
            status.update(label="已读 :white_check_mark:", state="complete", expanded=False)
        # st.html("<p style='font-size:10px; color:grey'>消息已送达</p>")
        # time.sleep(delayT)  # waiting for readreceipt

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            # Comprehension
            messages = [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream = True,
        )     
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


