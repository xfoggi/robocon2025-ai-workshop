import json
from openai import OpenAI

class RFAssistantsLibrary:
    def __init__(self):
        self.client = None
        self.assistant = None
        self.thread = None
        self.uploaded_file = None

    def set_openai_api_key(self, api_key):
        self.client = OpenAI(api_key=api_key)
        return

    def create_assistant(self, name, instructions, model, tools=None):
        if tools == None:
            tools = []

        self.assistant = self.client.beta.assistants.create(
            name = name,
            instructions = instructions,
            model = model,
            tools = tools
        )
        return
    
    def create_assistant_with_knowledge(self, name, instructions, model, tools=None, uploaded_file_id=None):
        if tools == None:
            tools = []

        if uploaded_file_id == None:
            uploaded_file_id = self.uploaded_file.id
        
        self.assistant = self.client.beta.assistants.create(
            name = name,
            instructions = instructions,
            model = model,
            tools = [{"type": "code_interpreter"}],
            tool_resources={
                "code_interpreter": {
                    "file_ids": [uploaded_file_id]
                }
            }
        )
        return

    def create_thread(self):
        self.thread = self.client.beta.threads.create()
        return

    def add_message_to_thread(self, role, content, thread_id=None):
        if thread_id == None:
            thread_id = self.thread.id

        self.client.beta.threads.messages.create(
            thread_id = thread_id,
            role = role,
            content = content
        )

        return

    def run_assistant(self, thread_id=None, assistant_id=None, instructions=""):
        if thread_id == None:
            thread_id = self.thread.id
        
        if assistant_id == None:
            assistant_id = self.assistant.id
        
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed': 
            messages = self.list_thread_messages(thread_id)
            print(messages)
        else:
            print(run.status)

        return messages

    def list_thread_messages(self, thread_id=None):
        return self.client.beta.threads.messages.list(
                thread_id=thread_id
            )
    
    def upload_file(self, filepath):
        self.uploaded_file = self.client.files.create(
            file=open(filepath, "rb"),
            purpose="assistants"
        )
        return
    
    def add_message_to_thread_with_file(self, role, content, uploaded_file_id = None, thread_id=None):
        if thread_id == None:
            thread_id = self.thread.id

        if uploaded_file_id == None:
            uploaded_file_id = self.uploaded_file.id

        self.client.beta.threads.messages.create(
            thread_id = thread_id,
            role = role,
            content = content,
            attachments=[
                {
                    "file_id": uploaded_file_id,
                    "tools": [{"type": "code_interpreter"}]
                }
            ]
        )

        return