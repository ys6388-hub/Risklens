import os
import time
from src.interfaces import BaseTargetAgent
import openai
import google.generativeai as genai


# ======================
# OpenAI Target (官方 SDK)
# ======================
class OpenAITarget(BaseTargetAgent):
    def __init__(self, model_name="gpt-4o"):
        self._model_name = model_name
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model_name

    @property
    def name(self):
        return f"OpenAI ({self._model_name})"

    def invoke(self, prompt):
        """使用 OpenAI 官方 ChatCompletion API"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI Error]: {str(e)}"


# ======================
# Google Gemini Target（官方 SDK）
# ======================
class GoogleTarget(BaseTargetAgent):
    def __init__(self, model_name="gemini-1.5-pro-latest"):
        self._model_name = model_name
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.client = genai.GenerativeModel(model_name)

    @property
    def name(self):
        return f"Google ({self._model_name})"

    def invoke(self, prompt):
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Gemini Error]: {str(e)}"


# ======================
# Mock Agent（测试用）
# ======================
class MockTarget(BaseTargetAgent):
    @property
    def name(self):
        return "Mock Agent (Test Mode)"

    def invoke(self, prompt):
        time.sleep(1)
        if "hate" in prompt.lower() or "violent" in prompt.lower():
            return "I cannot fulfill this request as it violates safety policies."
        return "Sure, here is the content..."


# ======================
# Agent Factory（必须存在）
# ======================
class AgentFactory:
    @staticmethod
    def get_available_agents():
        """返回所有支持的 Agent 列表"""
        return {
            "mock": MockTarget(),
            "openai-gpt4o": OpenAITarget(model_name="gpt-4o"),
            "gemini-pro": GoogleTarget(model_name="gemini-1.5-pro-latest"),
            "gemini-flash": GoogleTarget(model_name="gemini-1.5-flash-latest"),
        }

