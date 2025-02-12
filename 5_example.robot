*** Settings ***
Library    RFAssistantsLibrary.py

*** Variables ***
${assistant_name}    Math Tutor
${assistant_instruction}    You are a personal math tutor. Write and run code to answer math questions.
${assistant_model}    gpt-4o-mini
${assistant_tools}    [{"type": "code_interpreter"}]


*** Test Cases ***
Create assistant and run
    Set Openai Api Key  OPENAI_API_KEY_SECRET

    Create Assistant    ${assistant_name}    ${assistant_instruction}    ${assistant_model}    ${assistant_tools}

    Create Thread
    Add Message To Thread    user    10x + 5 = 15
    ${result}=    Run Assistant
    Log    ${result}

Create assistant and upload a file
    Set Openai Api Key  OPENAI_API_KEY_SECRET

    Create Assistant    ${assistant_name}    ${assistant_instruction}    ${assistant_model}    ${assistant_tools}

    Create Thread
    Upload File    test.txt
    Add Message To Thread With File    user    Compute all the equations in the included file.

    ${result}=    Run Assistant
    Log    ${result}

Create assistant with knowledge
    Set Openai Api Key  OPENAI_API_KEY_SECRET

    Upload File    test.txt

    Create Assistant With Knowledge    ${assistant_name}    ${assistant_instruction}    ${assistant_model}    ${assistant_tools}

    Create Thread
    Add Message To Thread    user    Evaluate the equations in the knowledge base.
    ${result}=    Run Assistant
    Log    ${result}