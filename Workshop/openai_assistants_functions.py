from openai import OpenAI
import requests

client = OpenAI(api_key="OPENAI_API_KEY_SECRET")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
},
{
    "type": "function",
    "function": {
        "name": "get_capital",
        "description": "Get capital city of a country.",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "Country like Finland, France, ..."
                }
            },
            "required": [
                "country"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}
]


assistant = client.beta.assistants.create(
    name = "Weather assistant",
    instructions="You help users understand what is the weather like in certain locations via custom fucntions.",
    tools=tools,
    model="gpt-4o-mini"
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What can you tell me about wheather in Finland."
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

while run.status == "requires_action":

    # Define the list to store tool outputs
    tool_outputs = []
    
    # Loop through each tool in the required action section
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        print(tool.function.name)
        if tool.function.name == "get_weather":
            latitude = 60.1699
            longitude = 24.9384
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
            print(response)
            data = response.json()       
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": str(data['current']['temperature_2m'])
            })
        elif tool.function.name == "get_capital":
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": "Helsinki."
            })
        else:
            print(tool.function.name)
    
    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
 
if run.status == 'completed':
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)


