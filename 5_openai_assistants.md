# OpenAI Assistants: Quickstart Guide

This guide walks you through using the OpenAI Assistants API to create an Assistant, configure its instructions and tools, set up a conversation thread, and send/receive messages. In addition, it explains how to upload files to a Thread versus a Knowledge Base, and highlights the differences between the two.

---

## Overview

A typical integration with the Assistants API involves the following steps:

1. **Create an Assistant:**  
   Define custom instructions, choose a model, and optionally enable tools (such as Code Interpreter or File Search). You can also attach files to the Assistant as resources for the tools (this is used as the Knowledge Base).

2. **Create a Thread:**  
   Start a conversation by creating a Thread when a user interacts with your Assistant.

3. **Add Messages:**  
   Add user messages (and optionally file attachments) to the Thread.

4. **Run the Assistant:**  
   Run the Assistant on the Thread to generate a response. The API uses the Assistant’s model and tools to process the conversation and produce an answer.

---

## Step 1: Create an Assistant

An **Assistant** represents an entity configured with instructions, a model, and optional tools. In this example, we create a personal math tutor with Code Interpreter enabled.

### Example: Create an Assistant

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o"
)
```

> **Note:**  
> Calls to the Assistants API require a beta HTTP header (`OpenAI-Beta: assistants=v2`), which is automatically handled if you’re using the official SDKs.

---

## Step 2: Create a Thread

A **Thread** represents a conversation session between a user and one or more Assistants. Create a Thread when the user initiates a conversation.

### Example: Create a Thread

```python
thread = client.beta.threads.create()
```

You can also use the corresponding JavaScript or cURL examples provided in the documentation if needed.

---

## Step 3: Add a Message to the Thread

User messages are added as Message objects within the Thread. These messages can include text and file attachments.

### Example: Add a Message

```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
```

Each message helps build the context that the Assistant will use when generating a response.

---

## Step 4: Run the Assistant

Once all messages have been added, create a **Run** to execute the Assistant on the Thread. The Assistant’s response will be added as a new Message.

### Example: Create and Poll a Run

For non-streaming usage, you can create a Run and poll until completion:

```python
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)
```

Alternatively, you can use streaming helpers to receive incremental updates as the Assistant generates its response.

---

## Uploading Files: Thread vs. Knowledge Base

### Uploading Files to a Thread

- **Purpose:**  
  Files uploaded to a Thread are typically attached to specific messages. They serve as immediate context for that particular conversation.
  
- **Usage:**  
  When a user needs the Assistant to analyze or process a file (e.g., an image or document), the file is attached to a message via the Thread.
  
- **Example:**  
  When creating a Thread message, include an attachment:
  
  ```python
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content="Please analyze the attached document.",
      attachments=[{"file_id": "file_abc123", "tools": [{"type": "code_interpreter"}]}]
  )
  ```

### Uploading Files to a Knowledge Base (Tool Resources)

- **Purpose:**  
  Files uploaded as part of the **Knowledge Base** are attached to the Assistant via the `tool_resources` parameter. These files are available to the Assistant’s tools (e.g., Code Interpreter or File Search) across multiple conversations.
  
- **Usage:**  
  Upload the file using the Files API with the `purpose` set to `assistants` and then reference the file ID in the Assistant’s `tool_resources`.
  
- **Example:**  
  1. **Upload the File:**

  ```python
  file = client.files.create(
      file=open("data.csv", "rb"),
      purpose="assistants"
  )
  ```

  2. **Create the Assistant with the File as a Resource:**

  ```python
  assistant = client.beta.assistants.create(
      name="Data Visualizer",
      instructions="You analyze .csv files and generate data visualizations.",
      model="gpt-4o",
      tools=[{"type": "code_interpreter"}],
      tool_resources={
          "code_interpreter": {
              "file_ids": [file.id]
          }
      }
  )
  ```

> **Difference Recap:**  
> - **Thread Attachments:** Files attached directly to a Thread are used for the context of that specific conversation.  
> - **Knowledge Base Files:** Files attached via `tool_resources` are part of the Assistant’s persistent resources and can be used across multiple runs and threads.
