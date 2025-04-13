## This is a tool that accesses the internet and retrieves information from a list of files and displays it in a window for 20 secs

from langchain.tools import BaseTool
import os
import tkinter as tk
import threading
from typing import Optional
from pydantic import Field
import time

class LocalFileDisplayTool(BaseTool):
    name: str = "LocalFileDisplayTool"
    description: str = "Reads local text files from a directory and shows their content in a popup window for 20 seconds.Fluent text, keep it short"
    
    def __init__(self):
        super().__init__()
    
    def _run(self, query: str) -> str:
        # Step 1: Read all text files from directory
        content_list = []
        directory_path = "data"  # Directory containing text files
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                if query.lower()[:5] not in filename.lower():
                    continue
                filepath = os.path.join(directory_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    content_list.append(f"File: {filename}\n\n{content[:500]}")  # limit to 500 chars for display

        combined_content = "\n\n---\n\n".join(content_list)

        # Step 2: Show in Window
        self.show_popup(combined_content)

        return "Displayed local text content."

    def show_popup(self, content: str):
        def popup():
            window = tk.Tk()
            window.title("Local File Content")

            text_widget = tk.Text(window, wrap="word")
            text_widget.insert("1.0", content)
            text_widget.pack(expand=True, fill="both")

            def close_after_delay():
                time.sleep(20)
                window.destroy()

            threading.Thread(target=close_after_delay, daemon=True).start()
            window.mainloop()

        popup_thread = threading.Thread(target=popup)
        popup_thread.start()
        popup_thread.join()

    async def _arun(self, query: str) -> str:
        # For async, we can just call the sync method
        return self._run(query)

if __name__ == "__main__":
    # Example usage
    tool = LocalFileDisplayTool()
    result = tool.run("loan_documents")
    print(result)