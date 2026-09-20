from datetime import datetime
from urllib.parse import parse_qs, urlparse
import requests
from .schema import BaseEpaperProvider, EpaperBatch


class EenaduProvider(BaseEpaperProvider):
    def can_handle(self, url: str) -> bool:
        return "eenadu.net" in url.lower()

    def fetch(self, url: str) -> EpaperBatch:
        params = parse_qs(urlparse(url).query)
        eid = params.get("eid", params.get("editionid", ["2"]))[0]
        date = params.get(
            "date",
            params.get(
                "edate",
                params.get("editiondate", [datetime.now().strftime("%d/%m/%Y")]),
            ),
        )[0]

        res = requests.get(
            "https://epaper.eenadu.net/Home/GetAllpages",
            params={"editionid": eid, "editiondate": date, "IsMag": 0},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
        )
        urls = [
            p.get("XHighResolution") or p.get("HighResolution")
            for p in res.json()
            if p.get("XHighResolution") or p.get("HighResolution")
        ]
        return EpaperBatch(source="eenadu", eid=eid, date=date, image_urls=urls)
