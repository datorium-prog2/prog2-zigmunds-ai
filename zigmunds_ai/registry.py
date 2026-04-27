from google.genai import types

from zigmunds_ai.tools import list_directory_files

# _ mainīgā nosaukuma sākumā nozīmē, ka tas ir "privāts"
# (nav ieteicams izmantot ārpus faila (moduļa))
_list_directory_files_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="list_directory_files",
            description="Fetches list of items in path (must be in current workplace directory)",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={"path": types.Schema(type=types.Type.STRING)},
                required=["path"],
            ),
        )
    ]
)

TOOLS = [_list_directory_files_tool]

TOOL_REGISTRY = {
    "list_directory_files": list_directory_files,
}
