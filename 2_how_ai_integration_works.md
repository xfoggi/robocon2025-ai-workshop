# How AI Integration Works

In this section, we'll learn how to integrate AI into your application using the latest OpenAI Python API library with the `gpt-4o-mini` model. We will cover environment setup, constructing conversation messages, making API calls, and maintaining context in multi-turn conversations.

---

## 1. Prerequisites

- **Python:** Ensure you have Python 3.8 or later installed.
- **OpenAI Python Library:** Install via pip:
  
  ```bash
  pip install openai
  ```

- **API Key:** Obtain your API key from OpenAI and store it in your environment (for example, by using a `.env` file or setting the `OPENAI_API_KEY` environment variable).

---

## 2. Setting Up Your Environment

### a. Importing the Library and Initializing the Client

In your Python script, import the necessary module and create an OpenAI client using your API key:

```python
import os
from openai import OpenAI

# Initialize the client with your API key from the environment variable.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# or without env variable
client = OpenAI(api_key="OPENAI_API_KEY")
```

---

## 3. Understanding the `gpt-4o-mini` Model

- **Model Overview:**  
  The `gpt-4o-mini` model is a variant optimized for specific tasks. It provides strong natural language understanding and generation capabilities while being tailored for performance and cost-effectiveness.
- **Usage:**  
  Specify this model when making your chat completion API calls.

---

## 4. Building a Conversation

### a. Constructing the Message Array

The OpenAI API uses a chat format where each message is an object with a `role` and `content`. The conversation history is maintained by sending the entire array of messages in order.

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How does AI integration work?"}
]
```

---

## 5. Making an API Call

### a. Creating a Chat Completion Request

Use the `client.chat.completions.create` method to send your conversation to the model:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
```

### b. Extracting and Displaying the Response

Access the generated response from the updated structure:

```python
assistant_reply = response.choices[0].message.content
print("Assistant:", assistant_reply)
```

---

## 6. Maintaining Context in Conversations

### a. Appending New User Messages

For multi-turn conversations, append each new user message (and include prior assistant responses if desired) to the `messages` array. This ensures the full conversation history is sent with each API call, allowing the model to generate context-aware responses.

```python
# Append a new user message to continue the conversation.
messages.append({"role": "user", "content": "Can you provide more details on how the API works?"})

# Make a follow-up API call with the updated conversation history.
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

assistant_reply = response.choices[0].message.content
print("Assistant (Follow-Up):", assistant_reply)
```

*Note:* The order of messages in the array is crucial. Always send them in chronological order (system → user → assistant → new user, etc.) to maintain proper context.

---

## 7. Error Handling and Best Practices

### a. Implementing Error Handling

Wrap your API calls in try-except blocks to gracefully handle any exceptions:

```python
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    assistant_reply = response.choices[0].message.content
    print("Assistant:", assistant_reply)
except Exception as e:
    print("An error occurred:", e)
```

### b. Monitor Token Usage and API Limits

- **Token Limits:** Both your input messages and the generated responses count toward your token usage.
- **Rate Limits:** Follow OpenAI's guidelines to avoid exceeding API rate limits. The library includes automatic retries for certain error types, but additional error handling may be necessary for your application.

---

## 8. Summary

- **Environment Setup:** Install the OpenAI Python API library and set your API key.
- **Client Initialization:** Use the new client-based syntax to create an `OpenAI` client.
- **Message Structure:** Build your conversation as an ordered list of messages with roles (`system`, `user`, `assistant`).
- **Context Preservation:** Maintain conversation context by including all previous messages in the API call.
- **Error Handling:** Implement try-except blocks and monitor token usage and rate limits.