import base64
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .schema import BaseEpaperProvider, EpaperBatch


class AndhraJyothyProvider(BaseEpaperProvider):
    KEY = b"abcdefghijklmnop"
    IV = b"abcdefghijklmnop"

    def can_handle(self, url: str) -> bool:
        return "andhrajyothy.com" in url.lower()

    def _decrypt(self, enc_b64: str) -> str:
        ciphertext = base64.b64decode(enc_b64)
        cipher = AES.new(self.KEY, AES.MODE_CBC, self.IV)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode("utf-8")

    def fetch(self, url: str) -> EpaperBatch:
        params = parse_qs(urlparse(url).query)
        eid = params.get("eid", ["182"])[0]
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        date = params.get("edate", [yesterday])[0]

        res = requests.post(
            "https://epaper.andhrajyothy.com/Home/GetAllpagespost",
            json={"editionid": eid, "editiondate": date, "email": ""},
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            timeout=30,
        )
        urls = []
        for p in res.json():
            enc = p.get("HrImageUrlJpg") or p.get("HrImageUrl")
            urls.append(self._decrypt(enc) if enc else p.get("MrImageUrl"))

        return EpaperBatch(source="andhrajyothy", eid=eid, date=date, image_urls=urls)
