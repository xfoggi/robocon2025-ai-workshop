from swarm import Swarm, Agent

client = Swarm()

english_agent = Agent(
    name="English Agent",
    instructions="You only speak English.",
)

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish.",
)

def transfer_to_spanish_agent():
    """Transfer spanish speaking users immediately."""
    return spanish_agent

def transfer_to_english_agent():
    """Transfer english speaking users immediately."""
    return english_agent


english_agent.functions.append(transfer_to_spanish_agent)
spanish_agent.functions.append(transfer_to_english_agent)

messages = [{"role": "user", "content": "Hola. ¿Como estás?"}]
response = client.run(agent=english_agent, messages=messages)

print(response.messages)

print(response.messages[-1]["content"])

messages.append({"role": "assistant", "content": response.messages[-1]["content"]})
messages.append({"role": "user", "content": "Hey, how are you?"})
response = client.run(agent=spanish_agent, messages=messages)

print(response.messages)

print(response.messages[-1]["content"])