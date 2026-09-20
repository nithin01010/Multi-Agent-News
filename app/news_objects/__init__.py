from .andhra_jyothy import AndhraJyothyProvider
from .eenadu import EenaduProvider
from .schema import BaseEpaperProvider, EpaperBatch

PROVIDERS: list[BaseEpaperProvider] = [EenaduProvider(), AndhraJyothyProvider()]


def fetch_epaper(url: str) -> EpaperBatch:
    for p in PROVIDERS:
        if p.can_handle(url):
            return p.fetch(url)
    raise ValueError(f"No provider found for URL: {url}")
