import json
import re
from bughunt.agent.history import ConversationHistory
from bughunt.agent.prompts.loader import load_prompt
from bughunt.tools.registry import call_tool, list_tools


def parse_react_response(text: str) -> dict:
    thought = re.search(r"Thought:\s*(.+?)(?=\nAction:|\nAnswer:|$)", text, re.DOTALL)
    action = re.search(r"Action:\s*(.+?)(?=\nThought:|\nObservation:|\nAnswer:|\Z)", text, re.DOTALL)
    answer = re.search(r"Answer:\s*(.+?)$", text, re.DOTALL)

    action_data = None
    parse_error = False

    if action:
        raw = action.group(1).strip()
        if raw != "null":
            try:
                action_data = json.loads(raw)
            except json.JSONDecodeError:
                parse_error = True

    return {
        "thought": thought.group(1).strip() if thought else None,
        "action": action_data,
        "answer": answer.group(1).strip() if answer else None,
        "parse_error": parse_error,
        "answer": answer.group(1).strip() if answer else None,
    }

class ReActLoop:
    def __init__(self, llm_client, max_steps: int = 10):
        self.llm = llm_client
        self.max_steps = max_steps
        self.history = ConversationHistory()
        system_prompt = load_prompt("react_agent")
        system_prompt = system_prompt + "\n\nAvailable tools:\n" + list_tools()
        self.history.add("system", system_prompt)

    def run(self, user_input: str) -> str:
        self.history.add("user", user_input)

        for step in range(self.max_steps):
            response = self.llm.chat(self.history.to_prompt())
            self.history.add("assistant", response)

            parsed = parse_react_response(response)

            for attempt in range(2):
                if not parsed["parse_error"]:
                    break
                self.history.add("user", 'Your Action was not valid JSON. Output ONLY a JSON object in this exact format: {"tool": "tool_name", "args": {}}')
                response = self.llm.chat(self.history.to_prompt())
                self.history.add("assistant", response)
                parsed = parse_react_response(response)

            if parsed["answer"]:
                return parsed["answer"]

            if parsed["action"]:
                observation = call_tool(parsed["action"]["tool"], parsed["action"]["args"])
                self.history.add("tool_result", f"Observation: {observation}")

        return "Max steps reached without an answer."