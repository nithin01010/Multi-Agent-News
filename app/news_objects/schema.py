from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EpaperBatch:
    source: str
    eid: str
    date: str
    image_urls: list[str]


class BaseEpaperProvider(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        pass

    @abstractmethod
    def fetch(self, url: str) -> EpaperBatch:
        pass
