from abc import ABC, abstractmethod


class BaseTargetAgent(ABC):
    """
    标准化接口：所有被测 Agent 必须继承此类。
    这确保了无论底层是 OpenAI, Gemini 还是 HuggingFace，
    对外表现的行为是一致的。
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """返回 Agent 的名称"""
        pass

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        核心方法：发送 prompt，返回 Agent 的回复(str)。
        """
        pass