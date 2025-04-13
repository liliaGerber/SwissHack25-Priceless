from langchain_core.tools import BaseTool


class UserContextReply(BaseTool):
    name: str = "UserContextReply"
    description: str = "Reads local text files from a directory and shows their content in a popup window for 20 seconds."

    def __init__(self):
        super().__init__()