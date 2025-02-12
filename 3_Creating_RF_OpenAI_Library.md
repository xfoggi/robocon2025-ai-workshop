# Creating RF OpenAI Library
Our goal is to create a single-file Python library that exposes keywords to:

- Set your OpenAI API key.
- Configure the model to use (e.g., `gpt-4o-mini`).
- Send a message to the OpenAI API and retrieve the assistant's response.

## Overview

We will create two main files:

1. **RFOpenAILibrary.py**  
   This file contains the implementation of our custom Robot Framework library. It will:
   - Define a class (e.g., `RFOpenAILibrary`) that initializes with a `None` OpenAI client and model.
   - Provide a keyword to set the OpenAI API key, which initializes the OpenAI client.
   - Provide a keyword to set the desired model.
   - Provide a keyword to send a message to the OpenAI API and return the assistant's reply.
   - Handle errors gracefully, returning informative messages if required inputs (such as API key or model) are missing.

2. **usage.robot**  
   This file is a Robot Framework test suite that demonstrates how to use the custom library. In the test suite, you will:
   - Import the `RFOpenAILibrary.py` as a library.
   - Use the provided keywords to:
     - Set the API key.
     - Set the model (e.g., `gpt-4o-mini`).
     - Send a message and log the response from the API.

## Implementation Details

### RFOpenAILibrary.py

- **Initialization:**  
  The library will initialize with properties for the API client and model (both initially set to `None`).

- **Setting the API Key:**  
  Create a method `set_openai_api_key(api_key)` that accepts the API key, initializes the OpenAI client using the latest OpenAI Python API library, and returns a confirmation.

- **Setting the Model:**  
  Create a method `set_model(model_name)` that stores the provided model name (e.g., `gpt-4o-mini`) and returns a confirmation.

- **Sending a Message:**  
  Create a method `send_message(message)` that:
  - Checks if the API key and model have been set.
  - Constructs a message payload.
  - Sends the message using the OpenAI client.
  - Extracts and returns the assistant's reply from the response.
  - Handles and returns errors if the API call fails.

### usage.robot

- **Import the Library:**  
  In your Robot Framework test suite, import the `RFOpenAILibrary.py` file.

- **Test Case Example:**  
  Write a test case that:
  - Uses the keyword to set the API key (ensure you replace any placeholder with your actual key).
  - Uses the keyword to set the model.
  - Uses the keyword to send a sample message (e.g., "Hello, how do I integrate AI?").
  - Logs the response from the API to verify the integration.

## Next Steps

1. **Implement the Library:**  
   Create and implement `RFOpenAILibrary.py` according to the details above.

2. **Create the Test Suite:**  
   Create `usage.robot` to demonstrate how the library's keywords are used in practice.

3. **Run and Validate:**  
   Execute the Robot Framework test suite to ensure that the library functions as expected.