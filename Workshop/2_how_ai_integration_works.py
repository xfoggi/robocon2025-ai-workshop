#!/usr/bin/env python3
"""
2_how_ai_integration_works.py

This script demonstrates how to integrate AI into your application using the latest OpenAI Python API library
with the gpt-4o-mini model. It builds an initial conversation, makes an API call, and then appends a follow-up
message to maintain context.
"""

import os
from openai import OpenAI

def main():
    # Initialize the OpenAI client using an API key from the environment variable.
    # It's recommended to store your API key in an environment variable (e.g., using python-dotenv)
    client = OpenAI(api_key="OPENAI_API_KEY_SECRET")
    
    # Build the initial conversation history
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Robot Framework?"}
    ]
    
    # Make the first API call with the initial conversation
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        print("Assistant:", assistant_reply)
    except Exception as e:
        print("Error during first API call:", e)
    
    return
    # Append a new user message to continue the conversation
    messages.append({"role": "user", "content": "Can you provide more details on Robot Framework Foundation?"})
    
    # Make a follow-up API call with the updated conversation context
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        print("Assistant (Follow-Up):", assistant_reply)
    except Exception as e:
        print("Error during follow-up API call:", e)

if __name__ == '__main__':
    main()