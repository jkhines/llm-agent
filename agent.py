import json
import subprocess
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
)
messages = []

tools = [{
    "type": "function",
    "function": {
        "name": "ping",
        "description": "Ping some host on the internet",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "The host to ping"},
            },
            "required": ["host"],
        },
    },
}]

def ping(host=""):
    print(f"Pinging {host}...")
    try:
        result = subprocess.run(
            ["ping", "-n", "3", host],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def call():
    print(f"Calling with messages: {messages}")
    return client.chat.completions.create(model="openai/gpt-5", messages=messages, tools=tools)

def process(line):
    print(f"Processing: {line}")
    messages.append({"role": "user", "content": line})
    response = call()
    
    # Handle tool calls
    while response.choices[0].message.tool_calls:
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        
        for tool_call in assistant_message.tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            result = ping(**function_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        
        response = call()
    
    assistant_message = response.choices[0].message
    messages.append(assistant_message)
    return assistant_message.content

def main():
    result = process("Describe our connectivity to Google")
    print(f">>> {result}\n")

if __name__ == "__main__":
    main()