#!/usr/bin/env python3
"""
This script demonstrates how to extend an OpenAI Assistant with files:
- Attach a file to a Thread message.
- Upload a file as a Knowledge Base resource and create an Assistant referencing it.

Ensure that the OPENAI_API_KEY environment variable is set.
"""

import os
from openai import OpenAI

def main():
    # Ensure the API key is available
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # --- Part 1: Using Files in a Thread ---
    print("Uploading file for thread attachment...")
    try:
        thread_file = client.files.create(
            file=open("Browser.html", "rb"),
            purpose="assistants"
        )
    except Exception as e:
        print("Error uploading file for thread:", e)
        return

    # Create a new Thread for the conversation
    try:
        thread = client.beta.threads.create()
    except Exception as e:
        print("Error creating thread:", e)
        return

    print("Adding message with file attachment to thread...")
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Please analyze the attached document.",
            attachments=[{
                "file_id": thread_file.id,
                "tools": [{"type": "code_interpreter"}]  # Optional: specify tools if needed.
            }]
        )
    except Exception as e:
        print("Error adding message to thread:", e)
        return

    # --- Part 2: Using Files in the Knowledge Base ---
    print("Uploading file for knowledge base...")
    try:
        kb_file = client.files.create(
            file=open("Browser.html", "rb"),
            purpose="assistants"
        )
    except Exception as e:
        print("Error uploading file for knowledge base:", e)
        return

    print("Creating an assistant with the knowledge base file attached...")
    try:
        assistant = client.beta.assistants.create(
            name="Data Visualizer",
            instructions="You are Robot Framework Browser Library expert, in your knowledge base you have all keywords definition.",
            model="gpt-4o",
            tools=[{"type": "code_interpreter"}],
            tool_resources={
                "code_interpreter": {
                    "file_ids": [kb_file.id]
                }
            }
        )
        print("Assistant created with ID:", assistant.id)
    except Exception as e:
        print("Error creating assistant with knowledge base file:", e)
        return

if __name__ == "__main__":
    main()