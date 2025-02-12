from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY_SECRET")

assistant = client.beta.assistants.create(
    name = "Robot Framework Browser Expert",
    instructions="You help users with RF Browser library, as they are mostly Selenium testers, explain how the keywords work differently in Browser Library.",
    tools=[],
    model="gpt-4o-mini"
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="How should I wait for element before I click on it?"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)


