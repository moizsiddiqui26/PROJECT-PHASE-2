import requests
import streamlit as st

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_chatbot_response(user_input):

    api_key = st.secrets["GROQ_API_KEY"]  # secure

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a crypto assistant helping users with investments, risk, and forecasting."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠ Error getting response"
