from datetime import datetime
import time
import requests

from config import API_KEY, IMAGE_MODEL

INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

DETAILED_NEWS_PROMPT = """You are an expert multilingual news translator and verbatim transcriber.
Analyze this Telugu newspaper page image and transcribe all articles.

DO NOT summarize, condense, shorten, or omit content. 
Translate and transcribe the EXACT, COMPLETE text of every article into English.

For EACH article on the page, provide:
1. **Headline**: Full English translation of the headline.
2. **Category / Section**: (e.g., Editorial, State, National, Politics, Economy).
3. **Full Article Content**: The complete, word-for-word translation of the article text from beginning to end, preserving every paragraph, quotation, name, date, and statistic.

Transcribe all stories visible on the page exhaustively."""


def get_today_page_urls(
    base_url: str = "https://epaper.eenadu.net",
    eid: int = 2,
    date: str = "17/09/2026",
) -> list[str]:
    target_date = date or datetime.now().strftime("%d/%m/%Y")

    res = requests.get(
        f"{base_url}/Home/GetAllpages",
        params={"editionid": eid, "editiondate": target_date, "IsMag": 0},
        headers={"User-Agent": "Mozilla/5.0"},
    )
    pages = res.json()

    return [
        f"{p['HighResolution'].rsplit('/', 1)[0]}/{p['SectionName'].lower()}_mr.jpg"
        for p in pages
        if p.get("SectionName") and p.get("HighResolution")
    ]


def extract_page_text(img_url: str, timeout_secs: int = 300, max_retries: int = 3) -> str:
    """
    Sends a single page image URL to the Vision model.
    If a request hangs past timeout_secs (300s), it stops and restarts the request.
    """
    payload = {
        "model": IMAGE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": DETAILED_NEWS_PROMPT,
                    },
                    {"type": "image_url", "image_url": {"url": img_url}},
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.2,
    }

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.post(INVOKE_URL, headers=HEADERS, json=payload, timeout=timeout_secs)
            if r.ok:
                return r.json()["choices"][0]["message"]["content"]
            print(f"        [!] HTTP {r.status_code}. Retrying ({attempt}/{max_retries})...")
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"        [!] Exceeded {timeout_secs}s or connection dropped ({e.__class__.__name__}). Retrying ({attempt}/{max_retries})...")
        except Exception as e:
            print(f"        [!] Unexpected error: {e}. Retrying ({attempt}/{max_retries})...")

        time.sleep(2)

    return f"Error: Page extraction failed after {max_retries} attempts."


def extract_content(
    base_url: str = "https://epaper.eenadu.net",
    eid: int = 2,
    date: str = "17/09/2026",
    limit: int = None,
) -> list[str]:
    urls = get_today_page_urls(base_url, eid, date)
    if limit:
        urls = urls[:limit]

    print(f"[*] Extracting text sequentially from {len(urls)} pages for date {date}...")
    total_start = time.perf_counter()
    results = []

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] Processing page...")
        page_start = time.perf_counter()

        text = extract_page_text(url, timeout_secs=300, max_retries=3)
        results.append(text)

        page_duration = time.perf_counter() - page_start
        print(f"    -> Done in {page_duration:.2f}s ({len(text)} chars)")
        time.sleep(1)

    total_duration = time.perf_counter() - total_start
    print(f"\n[*] All {len(urls)} pages completed in {total_duration:.2f}s ({total_duration/60:.2f} mins)")
    return results


# Example usage:
if __name__ == "__main__":
    print("Starting extraction")
    articles = extract_content(eid=2, date="17/09/2026")
    print(f"\n[+] Successfully extracted {len(articles)} pages.")