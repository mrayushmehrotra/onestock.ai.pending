from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
from utils.logger import logger

@dataclass
class AgentResult:
    agent_name: str
    success: bool
    data: Any
    error: Optional[str] = None

class BaseAgent(ABC):
    name: str = "BaseAgent"

    async def safe_run(self, *args, **kwargs) -> AgentResult:
        try:
            logger.info(f"Starting agent: {self.name}")
            data = await self.run(*args, **kwargs)
            return AgentResult(agent_name=self.name, success=True, data=data)
        except Exception as e:
            logger.error(f"Agent {self.name} failed: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return AgentResult(agent_name=self.name, success=False, data=None, error=str(e))

    @abstractmethod
    async def run(self, *args, **kwargs) -> Any:
        pass
