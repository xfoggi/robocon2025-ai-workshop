*** Settings ***
Library    RFAssistantsLibrary.py

*** Variables ***
${API_KEY}               OPENAI_API_KEY_SECRET
${ASSISTANT_NAME}        Math Tutor
${ASSISTANT_INSTRUCTIONS}   You are a personal math tutor. Write and run code to answer math questions.
${MODEL}                 gpt-4o
${TOOLS}                 [{"type": "code_interpreter"}]

*** Test Cases ***
OpenAI Assistant End-to-End Test
    # Set the OpenAI API key
    ${key_msg}=    Set OpenAI API Key    ${API_KEY}
    Log    ${key_msg}

    # Create an Assistant
    ${assistant_msg}=    Create Assistant    ${ASSISTANT_NAME}    ${ASSISTANT_INSTRUCTIONS}    ${MODEL}    ${TOOLS}
    Log    ${assistant_msg}

    # Create a new Thread for the conversation
    ${thread_msg}=    Create Thread
    Log    ${thread_msg}

    # Add a user message to the Thread
    ${msg_msg}=    Add Message To Thread    user    I need help solving the equation 3x + 11 = 14
    Log    ${msg_msg}

    # Run the Assistant on the Thread and wait for completion
    ${run_msg}=    Run Assistant    instructions=Please respond as a math tutor.
    Log    ${run_msg}

    # List all messages from the Thread
    ${all_messages}=    List Thread Messages
    Log    ${all_messages}

    