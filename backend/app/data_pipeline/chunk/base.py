from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional


class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str, callback: Optional[Callable] = None) -> List[Dict]:
        pass
