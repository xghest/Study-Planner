import os
import google.generativeai as genai
from .base import AIPlatform
from datetime import datetime
import json


class Gemini(AIPlatform):
    def __init__(self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        genai.configure(api_key=self.api_key)
        
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """
        Send a prompt to Gemini and return the text response.
        If system_prompt is provided, prepend it to the prompt.
        """
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        elif self.system_prompt:
            full_prompt = f"{self.system_prompt}\n\n{prompt}"

        response = self.model.generate_content(full_prompt)
        return response.text

    def plan_tasks(self, tasks: list, start_date: datetime.date) -> dict:
        """
        Build a daily plan from a list of TaskModel objects.
        Returns a dictionary with date strings as keys and list of task titles as values.
        """
        if not tasks:
            return {}

        # Build task list text
        task_list_text = ""
        for t in tasks:
            task_line = f"- {t.title} (due {t.due}): {t.description}"
            if getattr(t, "full_note", None):
                task_line += f" | Note: {t.full_note}"
            task_list_text += task_line + "\n"

        system_prompt = (
            "You are an AI task planner. I have the following tasks:\n\n"
            f"{task_list_text}\n"
            f"Create a daily plan starting from {start_date} until the latest due date.\n\n"
            "IMPORTANT RULES: ALWAYS schedule work starting from the earliest day (today), even if the due date is far away. Make sure to cover every task.\n\n"
            "Return ONLY valid JSON in this exact shape:\n"
            "{\n"
            "    \"YYYY-MM-DD\": [\"Task 1\", \"Task 2\"],\n"
            "    \"YYYY-MM-DD\": [\"Task 3\"],\n"
            "    ...\n"
            "}Note that the Task here should just be the titles with first letter capitalized\n\n"
            "No explanations. No extra text."
        )

        # Get AI response
        plan_text = self.chat("Create plan", system_prompt=system_prompt)

        # Strip code fences if present
        plan_text = plan_text.strip()
        if plan_text.startswith("```") and plan_text.endswith("```"):
            plan_text = "\n".join(plan_text.split("\n")[1:-1])

        # Convert to JSON
        try:
            plan_json = json.loads(plan_text)
        except json.JSONDecodeError:
            plan_json = {"raw_text": plan_text}

        return plan_json
