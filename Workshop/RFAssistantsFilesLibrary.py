#!/usr/bin/env python3
"""
A Robot Framework library to extend OpenAI Assistants with files.
Provides keywords to:
- Upload a file for thread attachment.
- Create a thread and attach a file.
- Upload a file for the knowledge base.
- Create an Assistant with a knowledge base file.
- Add a message to an existing thread.
- Run the Assistant on a thread.
- List messages from a thread.
"""

import os
import json
from openai import OpenAI

class RFAssistantsFilesLibrary:
    def __init__(self):
        self.client = None
        self.thread = None
        self.assistant = None

    def set_openai_api_key(self, api_key):
        """
        Set the OpenAI API key and initialize the client.
        """
        self.client = OpenAI(api_key=api_key)
        return "OpenAI API key set."

    def upload_file_for_thread(self, file_path):
        """
        Upload a file to be attached to a thread message.
        The file is uploaded with purpose "assistants".
        """
        try:
            file_obj = open(file_path, "rb")
        except Exception as e:
            return f"Error opening file: {e}"
        try:
            uploaded_file = self.client.files.create(
                file=file_obj,
                purpose="assistants"
            )
            return uploaded_file.id
        except Exception as e:
            return f"Error uploading file for thread: {e}"

    def create_thread_and_attach_file(self, file_id, message_text):
        """
        Create a new thread and add a message with a file attachment.
        """
        try:
            self.thread = self.client.beta.threads.create()
        except Exception as e:
            return f"Error creating thread: {e}"
        try:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message_text,
                attachments=[{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
            )
            return f"Thread created with ID: {self.thread.id} and file attached."
        except Exception as e:
            return f"Error adding message with file attachment: {e}"

    def upload_kb_file(self, file_path):
        """
        Upload a file to be used as a Knowledge Base file for an Assistant.
        The file is uploaded with purpose "assistants".
        """
        try:
            file_obj = open(file_path, "rb")
        except Exception as e:
            return f"Error opening file: {e}"
        try:
            uploaded_file = self.client.files.create(
                file=file_obj,
                purpose="assistants"
            )
            return uploaded_file.id
        except Exception as e:
            return f"Error uploading knowledge base file: {e}"

    def create_assistant_with_kb_file(self, name, instructions, model, file_id):
        """
        Create an Assistant with a Knowledge Base file attached.
        The file is referenced via the tool_resources parameter.
        """
        try:
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=[{"type": "code_interpreter"}],
                tool_resources={
                    "code_interpreter": {
                        "file_ids": [file_id]
                    }
                }
            )
            return f"Assistant created with ID: {self.assistant.id}"
        except Exception as e:
            return f"Error creating assistant with KB file: {e}"

    def add_message(self, role, content, thread_id=None):
        """
        Add a message to an existing thread.
        """
        t_id = thread_id if thread_id else (self.thread.id if self.thread else None)
        if not t_id:
            return "Error: Thread not found. Create a thread first."
        try:
            self.client.beta.threads.messages.create(
                thread_id=t_id,
                role=role,
                content=content
            )
            return f"Message added to thread {t_id}."
        except Exception as e:
            return f"Error adding message: {e}"

    def run_assistant(self, instructions="", thread_id=None, assistant_id=None):
        """
        Create a Run for the Assistant on a thread and poll until completion.
        """
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
        List all messages from a thread.
        """
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