from agents import Agent, function_tool, trace
from agents.mcp import MCPServerStdio
from agents import Runner
import random

from typing_extensions import TypedDict, Any

class Location(TypedDict):
    lat: float
    long: float


@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return random.choice([
        "It's sunny and warm.",
        "It's raining.",
        "It's snowing.",
        "It's cloudy.",
        "It's windy."
    ])



async def main():
    with trace("Get the weather workflow"):
        async with MCPServerStdio(
                params={
                    "command": "npx",
                    "args": ["-y", "tavily-mcp@0.1.4"],
                    "env": {
                        "TAVILY_API_URL": "https://api.tavily.com/v1",
                        "TAVILY_API_KEY": "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",
                    }
                }
            ) as server:
                tools = await server.list_tools()
                agent = Agent(
                    name="Travel Agent",
                    instructions="You provide help finding the best travel destinations.",
                    tools=[fetch_weather],
                    mcp_servers=[server],
                )
                result = await Runner.run(agent, "What's the weather like in Paris and is anything happening this month I should see? Make sure to check for May 2025 events.")
                print(result.final_output)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())