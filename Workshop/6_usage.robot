*** Settings ***
Library    RFAssistantsFilesLibrary.py

*** Variables ***
${API_KEY}               OPENAI_API_KEY_SECRET
${THREAD_FILE_PATH}      Browser.html
${KB_FILE_PATH}          Browser.html
${MESSAGE_TEXT}          Please analyze the attached document.
${ASSISTANT_NAME}        RF Browser Expert
${ASSISTANT_INSTRUCTIONS}    You are Robot Framework Browser library expert and you help explain how Browser library keywords works.
${MODEL}                 gpt-4o-mini

*** Test Cases ***
Test Thread File Attachment
    Set OpenAI API Key    ${API_KEY}
    ${file_id}=    Upload File For Thread    ${THREAD_FILE_PATH}
    Log    Uploaded file ID: ${file_id}
    ${thread_msg}=    Create Thread And Attach File    ${file_id}    ${MESSAGE_TEXT}
    Log    ${thread_msg}

Test Knowledge Base Assistant
    Set OpenAI API Key    ${API_KEY}
    ${kb_file_id}=    Upload KB File    ${KB_FILE_PATH}
    Log    Uploaded KB file ID: ${kb_file_id}
    ${assistant_msg}=    Create Assistant With KB File    ${ASSISTANT_NAME}    ${ASSISTANT_INSTRUCTIONS}    ${MODEL}    ${kb_file_id}
    Log    ${assistant_msg}

Test Assistant Response With KB File
    [Documentation]    Create an assistant with a KB file, then send a message and run the assistant to verify it uses the KB file.
    Set OpenAI API Key    ${API_KEY}
    ${kb_file_id}=    Upload KB File    ${KB_FILE_PATH}
    Log    Uploaded KB file ID: ${kb_file_id}
    ${assistant_msg}=    Create Assistant With KB File    ${ASSISTANT_NAME}    ${ASSISTANT_INSTRUCTIONS}    ${MODEL}    ${kb_file_id}
    Log    ${assistant_msg}
    # Create a new thread (for conversation without file attachment, since KB file is persistent)
    ${dummy_file_id}=    Upload File For Thread    ${THREAD_FILE_PATH}
    ${thread_msg}=    Create Thread And Attach File    ${dummy_file_id}    ${ASSISTANT_INSTRUCTIONS}
    Log    ${thread_msg}
    ${msg_result}=    Add Message    user    "Using the knowledge base, answer: What keywords can I use to click on elements?"
    Log    ${msg_result}
    ${run_result}=    Run Assistant    instructions=${ASSISTANT_INSTRUCTIONS}
    Log    ${run_result}
    ${all_messages}=    List Thread Messages
    Log    ${all_messages}