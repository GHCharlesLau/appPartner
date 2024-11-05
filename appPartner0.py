# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:36:34 2024

For pretest: Find out the threshold of delayed response. 

@author: liuyu
"""

import streamlit as st
from openai import OpenAI
import numpy as np
import random, time
from datetime import datetime, timedelta


# Streamed response emulator (generator function)
def response_generator():
    response = "对话结束，感谢您的参与 :)"
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

delayTlist = [0, 1, 3, 5, 10, 15, 20, 25, 30, 40, 50, 60, 90, 120, 150, 180]
# delayTlist.extend(range(5, 181, 5))
delayTlist.reverse()  # Reverse the list to avoid performance decrease if using pop(0).

# delayT2 = [0, 1, 3, 5]

# Add delayTlist into the session_state
if "delayTlist" not in st.session_state:
    st.session_state.delayTlist = delayTlist
    
# Add responseSpeed into the session state
if "responseSpeeds" not in st.session_state:
    st.session_state["responseSpeeds"] = []


# Display chat messages from history on app rerun (eliminate the system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# delayT = random.randint(3, 20)  # randomize deplayed time interval
try:
    delayT = st.session_state["delayTlist"].pop()  # pop up delayT orderly in delayTlist in the dicitionary-like session_state.
except Exception:
    pass  # Ignore all exceptions

# Accept user input and React to the user
if prompt := st.chat_input("在干啥？"):  # We used the := operator to assign the user's input to the prompt variable and checked if it's not None in the same line.
    # Time display at first
    nowT = datetime.now().strftime("%H:%M:%S")  # Get current time
    st.write(f"<p style='backgroud-color:gray; text-align:center; font-size:10px'> {nowT} </p>", unsafe_allow_html=True)  # Display current time

    # Display user message in chat message container
    with st.chat_message("user", avatar=":material/account_circle:"):
        st.markdown(prompt)
     
    # col1, col2 = st.columns([3,1])  # split the container into two columns
    # with col2:
    #     time.sleep(3)
    #     st.status(label="已读 :white_check_mark:", state="complete", expanded=False)
        # with st.status("消息发送中...", expanded=True) as status:
        #     time.sleep(1)
        #     status.update(label="消息已送达", state="complete", expanded=True)
        #     time.sleep(2)
        #     status.update(label="已读 :white_check_mark:", state="complete", expanded=False)  # Set the readreceipt
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": ":material/account_circle:"})  # Add user message to chat history
    
    try:
        time.sleep(delayT)  # waiting for response
    except Exception:
        pass
    
    nowT = datetime.now().strftime("%H:%M:%S")  # Get current time
    st.write(f"<p style='backgroud-color:gray; text-align:center; font-size:10px'> {nowT} </p>", unsafe_allow_html=True)  # Display current time
    
    # Display assistant response in chat message container
    if len(st.session_state.messages) <= 30:  # Allow at most 20-turn conversation
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
        
        # Request participants to rate the response speed.
        time.sleep(2)
        col1, col2 = st.columns([1, 1])
        with col2:
            st.write("*请对虚拟对象的回复速度打分。*")
        #     responseSpeed = st.slider(
        #         label="*你认为虚拟对象的回复在多大程度上是不及时的？（1=非常及时；7=非常不及时）*", 
        #         min_value=1, 
        #         max_value=7, 
        #         value=4)
        # st.session_state.responseSpeeds.append(responseSpeed)  # Archive the rating marks into the session state
        
    else:
        with st.chat_message("assistant", avatar=":material/face:"):
            response = st.write_stream(response_generator())  # When exceeding conversation turns
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": ":material/face:"})
    
    


