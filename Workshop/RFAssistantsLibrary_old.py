#!/usr/bin/env python3
"""
RFAssistantsLibrary.py

A Robot Framework library for interacting with the OpenAI Assistants API.
This library provides keywords to:
- Set the OpenAI API key.
- Create an Assistant.
- Create a Thread.
- Add a Message to a Thread.
- Run the Assistant (create a Run and poll until completion).
- List all messages from a Thread.
"""

import json
from openai import OpenAI

class RFAssistantsLibrary:
    def __init__(self):
        self.client = None
        self.assistant = None
        self.thread = None

    def set_openai_api_key(self, api_key):
        """
        Set the OpenAI API key and initialize the client.

        Arguments:
        - api_key: Your OpenAI API key.

        Returns:
        - A confirmation message.
        """
        self.client = OpenAI(api_key=api_key)
        return "OpenAI API key set."

    def create_assistant(self, name, instructions, model, tools=None):
        """
        Create an Assistant with the given parameters.

        Arguments:
        - name: The name of the Assistant.
        - instructions: Custom instructions for the Assistant.
        - model: The model to use (e.g., 'gpt-4o').
        - tools: (Optional) A JSON string representing a list of tools to enable (e.g., '[{"type": "code_interpreter"}]').

        Returns:
        - A confirmation message including the Assistant ID.
        """
        if self.client is None:
            return "Error: OpenAI API client not initialized. Set the API key first."
        tool_list = None
        if tools:
            try:
                tool_list = json.loads(tools)
            except Exception as e:
                return f"Error parsing tools JSON: {e}"
        try:
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=tool_list
            )
            return f"Assistant created with ID: {self.assistant.id}"
        except Exception as e:
            return f"Error creating assistant: {e}"

    def create_thread(self):
        """
        Create a new Thread for a conversation.

        Returns:
        - The Thread ID.
        """
        if self.client is None:
            return "Error: OpenAI API client not initialized. Set the API key first."
        try:
            self.thread = self.client.beta.threads.create()
            return f"Thread created with ID: {self.thread.id}"
        except Exception as e:
            return f"Error creating thread: {e}"

    def add_message_to_thread(self, role, content, thread_id=None):
        """
        Add a message to a Thread.

        Arguments:
        - role: The role of the sender (e.g., "user").
        - content: The text content of the message.
        - thread_id: (Optional) The Thread ID. If not provided, uses the current thread.

        Returns:
        - A confirmation message.
        """
        if self.client is None:
            return "Error: OpenAI API client not initialized."
        t_id = thread_id if thread_id else (self.thread.id if self.thread else None)
        if not t_id:
            return "Error: Thread not found. Create a thread first."
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=t_id,
                role=role,
                content=content
            )
            return f"Message added to thread {t_id}."
        except Exception as e:
            return f"Error adding message: {e}"

    def run_assistant(self, thread_id=None, assistant_id=None, instructions=""):
        """
        Create a Run for the Assistant on a Thread and poll until completion.

        Arguments:
        - thread_id: (Optional) The Thread ID. If not provided, uses the current thread.
        - assistant_id: (Optional) The Assistant ID. If not provided, uses the current assistant.
        - instructions: (Optional) Instructions to override the Assistant's default instructions.

        Returns:
        - A summary of the Run, including its status.
        """
        if self.client is None:
            return "Error: OpenAI API client not initialized."
        t_id = thread_id if thread_id else (self.thread.id if self.thread else None)
        a_id = assistant_id if assistant_id else (self.assistant.id if self.assistant else None)
        if not t_id:
            return "Error: Thread not found. Create a thread first."
        if not a_id:
            return "Error: Assistant not found. Create an assistant first."
        try:
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=t_id,
                assistant_id=a_id,
                instructions=instructions
            )
            return f"Run completed with status: {run.status}"
        except Exception as e:
            return f"Error running assistant: {e}"

    def list_thread_messages(self, thread_id=None):
        """
        List all messages from a Thread.

        Arguments:
        - thread_id: (Optional) The Thread ID. If not provided, uses the current thread.

        Returns:
        - A string listing each message's role and content.
        """
        if self.client is None:
            return "Error: OpenAI API client not initialized."
        t_id = thread_id if thread_id else (self.thread.id if self.thread else None)
        if not t_id:
            return "Error: Thread not found."
        try:
            messages = self.client.beta.threads.messages.list(thread_id=t_id)
            output = ""
            for msg in messages.data:
                output += f"{msg.role}: {msg.content}\n"
            return output
        except Exception as e:
            return f"Error listing messages: {e}"