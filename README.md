# AI Agent with Tool Calling

A simple AI agent implementation that demonstrates function calling capabilities using OpenAI's API through OpenRouter.

## Source

This project is based on the fly.io article ["You Should Write An Agent"](https://fly.io/blog/everyone-write-an-agent/), which provides a tutorial on building a basic AI agent that can execute functions.

## API Implementation Notes

### Original vs. Current Implementation

**Original Article**: The fly.io article demonstrates using OpenAI's **Responses API**:
```python
client.responses.create(model="gpt-5", input=context, tools=tools)
```

**This Implementation**: Uses OpenAI's **Chat Completions API**:
```python
client.chat.completions.create(model="openai/gpt-4o", messages=messages, tools=tools)
```

### Justification for Change

1. This project uses OpenRouter rather than OpenAI. OpenRouter has better support for the standard Chat Completions API.
2. Chat Completions API is more widely documented and supported across providers.
3. The Chat Completions API has a well-established tool/function calling pattern that's compatible with multiple providers.

### Key Differences

| Aspect | Responses API | Chat Completions API |
|--------|---------------|---------------------|
| Context parameter | input | messages |
| Response structure | response.output | response.choices[0].message |
| Tool calls | item.type == "function_call" | message.tool_calls |
| Tool responses | Custom format | role: "tool" messages |

## Setup

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenRouter API key

### Installation

1. Install dependencies:
```powershell
uv sync
```

2. Set your API key as an environment variable:
```powershell
$env:OPENAI_API_KEY = "your-openrouter-api-key"
```

## Usage

Run the agent:
```powershell
uv run agent.py
```

### Adding More Tools

Tools are defined in the tools list. Each tool follows the OpenAI function calling schema. I'd like to add more tools, such as an HTTP site verification tool.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "your_function_name",
        "description": "Clear description for the LLM",
        "parameters": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "Parameter description"
                },
            },
            "required": ["param_name"],
        },
    },
}]
```

Then implement the Python function and add it to the tool execution logic in process().

## Troubleshooting

### API Key Issues
- Make sure `OPENAI_API_KEY` is set in your environment
- Verify your OpenRouter account has credits or use a free model. Qwen3 is pretty good!

### No Tool Calls When Expected
- Make tool descriptions more explicit
- Ensure the model supports function calling
- Check if the query clearly requires the tool

## License

This is a demonstration project based on the fly.io tutorial. Feel free to use and modify as needed.

## References

- [Original fly.io Article](https://fly.io/blog/everyone-write-an-agent/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

