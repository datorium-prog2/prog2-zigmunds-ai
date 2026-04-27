from google import genai
from google.genai import types

from zigmunds_ai.registry import TOOL_REGISTRY, TOOLS


class AgentSession:

    SYSTEM_INSTRUCTIONS = """
        You are a cranky senior developer named Zigmunds, who hates everyone.
        You are very un-funny and nobody likes your jokes or you.
        You are heplful though, and do what is asked of you as a senior developer.
        You reply ONLY Latvian.
        """

    # __init__ klasē ir klases konstruktors
    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.config = types.GenerateContentConfig(
            system_instruction=AgentSession.SYSTEM_INSTRUCTIONS, tools=TOOLS
        )
        self.model = model

        self.running = False
        self.history = []
        self.user_turn = True

    def run(self):
        self.running = True

        while self.running:
            self._run_turn()

        print("Exiting the program.")

    def _run_turn(self):
        if self.user_turn:
            self._read_user_message()

        response = self._get_model_response()
        self._add_model_response(response)

        function_call = self._get_function_call(response)
        if function_call:
            self._handle_function_call(function_call)
            self.user_turn = False
        else:
            print(response.text)
            self.user_turn = True

    def _read_user_message(self):
        user_prompt = input("Enter your message: ")

        if user_prompt.startswith("/exit"):
            self.running = False
            return

        user_message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_prompt)]
        )
        self.history.append(user_message)

    def _get_model_response(self):
        return self.client.models.generate_content(
            model=self.model, contents=self.history, config=self.config
        )

    def _get_function_call(self, response):
        if response.candidates[0].content.parts[0].function_call:  # type: ignore
            return response.candidates[0].content.parts[0].function_call

        return None

    def _handle_function_call(self, function_call):
        function_result = TOOL_REGISTRY[function_call.name](**function_call.args)  # type: ignore
        function_response = types.Part.from_function_response(
            name=str(function_call.name),
            response={"result": function_result},
        )
        self.history.append(function_response)

    def _add_model_response(self, response):
        self.history.append(response.candidates[0].content)
