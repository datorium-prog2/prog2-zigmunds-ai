import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from zigmunds_ai.tools import list_directory_files


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

config = types.GenerateContentConfig(system_instruction=system_instruction, tools=TOOLS)

client = genai.Client(api_key=api_key)

history = []
user_turn = True

while True:

    if user_turn:
        user_prompt = input("Enter your prompt (/exit to quit): ")

        if user_prompt.startswith("/exit"):
            print("Exiting the program.")
            sys.exit(0)

        user_message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_prompt)]
        )
        history.append(user_message)

    response = client.models.generate_content(
        model=model or "gemini-flash-lite-latest", contents=history, config=config
    )
    history.append(response.candidates[0].content)  # type: ignore

    if response.candidates[0].content.parts[0].function_call:  # type: ignore
        function_call = response.candidates[0].content.parts[0].function_call  # type: ignore
        function_result = TOOL_REGISTRY[function_call.name](**function_call.args)  # type: ignore
        function_response = types.Part.from_function_response(
            name=str(function_call.name),
            response={"result": function_result},
        )
        history.append(function_response)
        user_turn = False

    else:
        print(response.text)
        user_turn = True
