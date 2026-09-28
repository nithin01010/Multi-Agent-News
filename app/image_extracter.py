from concurrent.futures import ThreadPoolExecutor, as_completed
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


def extract_page_text(
    img_url: str, timeout_secs: int = 300, max_retries: int = 3
) -> str:
    """Sends a single page image URL to the Vision model with retries."""
    payload = {
        "model": IMAGE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": DETAILED_NEWS_PROMPT},
                    {"type": "image_url", "image_url": {"url": img_url}},
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.2,
    }

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.post(
                INVOKE_URL, headers=HEADERS, json=payload, timeout=timeout_secs
            )
            if r.ok:
                return r.json()["choices"][0]["message"]["content"]
            print(
                f"        [!] HTTP {r.status_code}. Retrying ({attempt}/{max_retries})..."
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(
                f"        [!] Exceeded {timeout_secs}s or connection dropped ({e.__class__.__name__}). Retrying ({attempt}/{max_retries})..."
            )
        except Exception as e:
            print(
                f"        [!] Unexpected error: {e}. Retrying ({attempt}/{max_retries})..."
            )
        time.sleep(2)

    return f"Error: Page extraction failed after {max_retries} attempts."

def extract_from_urls(urls: list[str], max_workers: int = 4) -> list[str]:
    print(f"[*] Extracting text concurrently from {len(urls)} page images...")
    start_time = time.perf_counter()

    results_indexed: dict[int, str] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(extract_page_text, u): i for i, u in enumerate(urls)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                text = future.result()
                results_indexed[idx] = text
                print(f"    -> Completed image {idx + 1}/{len(urls)} ({len(text)} chars)")
            except Exception as e:
                print(f"    [!] Error extracting image {idx + 1}: {e}")
                results_indexed[idx] = f"Error: {e}"

    duration = time.perf_counter() - start_time
    print(f"[*] Extraction of {len(urls)} pages completed in {duration:.2f}s ({duration/60:.2f} mins)")
    return [results_indexed[i] for i in range(len(urls))]