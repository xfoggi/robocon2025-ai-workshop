import os
import csv
from datetime import datetime
from swarm import Swarm, Agent
from swarm.repl import run_demo_loop
import requests

FILE_NAME = "test_results.csv"
DISCORD_HOOK = "https://discord.com/api/webhooks/" #CHANGE THIS

# Function to store a test result with datetime in a CSV file.
def store_test_result(test_name, status):
    now = datetime.now().isoformat(timespec="seconds")
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["test_name", "status", "datetime"])
        writer.writerow([test_name, status, now])
    return f"Stored result: {test_name} - {status} at {now}"

# Function to retrieve all test results and format them as a detailed Markdown table including time.
def get_test_stats():
    if not os.path.isfile(FILE_NAME):
        return "No test results available."
    rows = []
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    if not rows:
        return "No test results available."
    md_table = "| Test Name | Status | Time |\n|-----------|--------|------|\n"
    for row in rows:
        md_table += f"| {row['test_name']} | {row['status']} | {row['datetime']} |\n"
    return md_table

def send_to_discord(message: str):
    url = DISCORD_HOOK
    data = {"content": f"```md\n{message}\n```"}
    response = requests.post(url, json=data)
    if response.status_code != 204:
         print("Failed to send message to discord: ", response.status_code, response.text)
    else:
         print("Message sent successfully!")

triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which agent is best suited to handle the user's request, and transfer the conversation to that agent imidietly. New tests should go to Store agent, Reports to Stats agent and sending to Discord agent",
)

store_agent = Agent(
    name="Store Agent",
    instructions=(
        "You store a new test result into the file-based storage system. "
        "Extract the test name and status from the user's message (formatted as 'TestName, STATUS'). "
        "The status should be saved as PASS or FAIL, if user provides it differently, transfer it to standard."
    ),
    functions=[store_test_result],
)


stats_agent = Agent(
    name="Stats Agent",
    instructions=(
        "You retrieve all stored test results and format them into a detailed Markdown table. "
        "The table should include Test Name, Status, and Time."
    ),
    functions=[get_test_stats]
)

discord_agent = Agent(
    name="Discord Agent",
    instructions=(
        "You retrieve all stored test results and format them into a detailed Markdown table. "
        "The table should include Test Name, Status, and Time."
        "Then you send the message to discord channel."
    ),
    functions=[get_test_stats,send_to_discord]
)

def transfer_to_store():
    return store_agent

def transfer_to_stats():
    return stats_agent

def transfer_to_discord_sender():
    return discord_agent

triage_agent.functions = [transfer_to_store, transfer_to_stats, transfer_to_discord_sender]
stats_agent.functions.append(transfer_to_store)
store_agent.functions.append(transfer_to_stats)
store_agent.functions.append(transfer_to_discord_sender)

def main():
    run_demo_loop(triage_agent, stream=True)

if __name__ == "__main__":
    main()
