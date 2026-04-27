import os
import sys

from dotenv import load_dotenv

from zigmunds_ai.agent import AgentSession

# .env failā your_api_key_here vietā jābūt jūsu GEMINI API atslēgai
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash-lite"

if not api_key:
    print("GEMINI_API_KEY is not set.")
    sys.exit(1)

agent_session = AgentSession(api_key, model)
agent_session.run()
