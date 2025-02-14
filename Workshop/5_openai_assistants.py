"""
assistants_example.py

This script demonstrates how to:
1. Create an Assistant (e.g., a personal math tutor).
2. Create a Thread (start a conversation).
3. Add a Message to the Thread.
4. Create a Run to generate a response from the Assistant.

Note: This example uses the beta endpoints of the OpenAI Assistants API.
"""

import os
from openai import OpenAI

def main():
    # Ensure the API key is available
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set the OPENAI_API_KEY environment variable.")
        return

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Step 1: Create an Assistant
    print("Creating Assistant...")
    try:
        assistant = client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4o"
        )
        print("Assistant created with ID:", assistant.id)
    except Exception as e:
        print("Error creating assistant:", e)
        return

    # Step 2: Create a Thread (start a conversation)
    print("Creating Thread...")
    try:
        thread = client.beta.threads.create()
        print("Thread created with ID:", thread.id)
    except Exception as e:
        print("Error creating thread:", e)
        return

    # Step 3: Add a Message to the Thread
    print("Adding a message to the Thread...")
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="I need to solve the equation 3x + 11 = 14. Can you help me?"
        )
        print("Message added to Thread.")
    except Exception as e:
        print("Error adding message to thread:", e)
        return

    # Step 4: Create a Run to process the conversation
    print("Creating and polling a Run...")
    try:
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please respond as a math tutor."
        )
    except Exception as e:
        print("Error creating or polling run:", e)
        return

    # Check Run status and output messages
    if run.status == "completed":
        print("Run completed. Retrieving messages from the Thread:")
        try:
            # Retrieve all messages from the thread
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for msg in messages.data:
                # Print each message's role and content
                print(f"{msg.role}: {msg.content}")
        except Exception as e:
            print("Error retrieving messages:", e)
    else:
        print("Run did not complete. Status:", run.status)

if __name__ == "__main__":
    main()