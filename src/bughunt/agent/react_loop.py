import json
import re
from bughunt.agent.history import ConversationHistory
from bughunt.agent.prompts.loader import load_prompt

def parse_react_response(text: str) -> dict:
    thought = re.search(r"Thought:\s*(.+?)(?=\nAction:|\nAnswer:|$)", text, re.DOTALL)
    action = re.search(r"Action:\s*(\{.+\}|null)", text, re.DOTALL)
    answer = re.search(r"Answer:\s*(.+?)$", text, re.DOTALL)

    return {
        "thought": thought.group(1).strip() if thought else None,
        "action": json.loads(action.group(1)) if action and action.group(1) != "null" else None,
        "answer": answer.group(1).strip() if answer else None,
    }

class ReActLoop:
    def __init__(self, llm_client, max_steps: int = 10):
        self.llm = llm_client
        self.max_steps = max_steps
        self.history = ConversationHistory()
        system_prompt = load_prompt("react_agent")
        self.history.add("system", system_prompt)

    def run(self, user_input: str) -> str:
        self.history.add("user", user_input)

        for step in range(self.max_steps):
            response = self.llm.chat(self.history.to_prompt())
            self.history.add("assistant", response)

            parsed = parse_react_response(response)

            if parsed["answer"]:
                return parsed["answer"]

            if parsed["action"]:
                observation = "Tool not implemented yet."
                self.history.add("tool_result", f"Observation: {observation}")

        return "Max steps reached without an answer."