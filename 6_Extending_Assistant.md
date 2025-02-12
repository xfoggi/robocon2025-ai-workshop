# Extending Assistant with Files (Thread & Knowledge Base)

## Introduction

In many scenarios, you may need to provide additional context or resources to your Assistant by including files. There are two primary approaches:

- **Thread Attachments:**  
  Files attached directly to a conversation (Thread). These files provide context specific to that conversation and are used for one-time interactions.

- **Knowledge Base Files:**  
  Files uploaded as part of the Assistant’s persistent resources using the `tool_resources` parameter. These files are part of the Assistant’s long-term knowledge base and can be referenced across multiple threads or runs.

This guide explains how to extend your Assistant with files using both methods and highlights their differences.

---

## 1. Using Files in a Thread

Files attached to a Thread are included in a message to provide immediate context for that specific conversation. For example, if a user wants the Assistant to analyze a document or image during a conversation, the file is attached to the message.

### Example: Attaching a File to a Thread Message

```python
# Assume `client` is an instance of OpenAI and `thread` has been created.
# First, upload a file and obtain its file ID.
uploaded_file = client.files.create(
    file=open("example_document.pdf", "rb"),
    purpose="assistants"
)

# Then, add a message to the thread with the file attachment.
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Please analyze the attached document.",
    attachments=[{
        "file_id": uploaded_file.id,
        "tools": [{"type": "code_interpreter"}]  # Optional: specify tools if needed.
    }]
)
```

---

## 2. Using Files in the Knowledge Base

Files added to the Knowledge Base become part of the Assistant’s persistent resources. These files are uploaded using the Files API with the purpose set to `"assistants"` and then referenced in the Assistant’s configuration (via the `tool_resources` parameter). This approach is ideal for reference materials or data that the Assistant should have ongoing access to across multiple conversations.

### Example: Adding a File to the Assistant’s Knowledge Base

```python
# Upload a file intended for persistent use.
knowledge_file = client.files.create(
    file=open("data_reference.csv", "rb"),
    purpose="assistants"
)

# Create the Assistant with the file attached as a persistent resource.
assistant = client.beta.assistants.create(
    name="Data Visualizer",
    instructions="You analyze CSV files to generate data visualizations.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [knowledge_file.id]
        }
    }
)
```

---

## Differences Between Thread Attachments and Knowledge Base Files

- **Thread Attachments:**
  - Attached directly to a message within a Thread.
  - Provide context specific to that conversation.
  - Used for one-time or immediate interactions.
  - Not persistently linked to the Assistant’s configuration.

- **Knowledge Base Files:**
  - Uploaded as part of the Assistant’s persistent resources.
  - Specified during Assistant creation (or modification) via the `tool_resources` parameter.
  - Available across multiple threads and runs.
  - Ideal for reference data, documentation, or any resources that should be accessible over time.

---

## Conclusion

Extending an Assistant with files enhances its ability to process rich, contextual information. Use thread attachments for conversation-specific files and Knowledge Base files for persistent, cross-session resources.

Experiment with both approaches to determine which best fits your application’s needs.

Happy integrating with OpenAI Assistants!