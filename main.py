import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_weather(city):
    return {"city": city, "temperature": 17}


load_dotenv()
# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    print("GEMINI_API_KEY is not set.")
    sys.exit(1)

system_instruction = """
        You are a cranky senior developer named Zigmunds, who hates everyone.
        You are very un-funny and nobody likes your jokes or you.
        You are heplful though, and do what is asked of you as a senior developer.
        You reply ONLY Latvian.
        """

tools = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Fetches weather data for a city",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={"city": types.Schema(type=types.Type.STRING)},
                required=["city"],
            ),
        )
    ]
)

TOOL_REGISTRY = {"get_weather": get_weather}

config = types.GenerateContentConfig(
    system_instruction=system_instruction, tools=[tools]
)

client = genai.Client(api_key=api_key)

while True:
    user_prompt = input("Enter your prompt (/exit to quit): ")

    if user_prompt.startswith("/exit"):
        print("Exiting the program.")
        sys.exit(0)

    response = client.models.generate_content(
        model=model or "gemini-flash-lite-latest", contents=user_prompt, config=config
    )

    if response.candidates[0].content.parts[0].function_call:  # type: ignore
        function_call = response.candidates[0].content.parts[0].function_call  # type: ignore
        print(f"Function call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        result = TOOL_REGISTRY[function_call.name](**function_call.args)  # type: ignore
        print(result)
    else:
        print(response.text)
