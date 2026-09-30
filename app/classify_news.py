import json
import re
from config import API_KEY, MODEL
from openai import OpenAI

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY)


def _clean_and_parse_json(content: str) -> dict:
    if not content:
        return {}
    content = content.strip()
    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {}


def _classify_single_batch(batch_items: list[str], domains: list[str]) -> dict[str, list[str]]:
    prompt = f"""
    Categorize the following news items only into these allowed
    domains: {domains}
    News items:
    {batch_items}
    . Classify the news into only these strict domains, add all others news in "others" : []...
    If duplicate news occurs, repeat them, no need to remove duplicates.
    Return ONLY a valid JSON object with domain names as keys and lists of news as values.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a news classification assistant. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        timeout=120,
    )

    content = response.choices[0].message.content or ""
    parsed = _clean_and_parse_json(content)
    return parsed.get("categories", parsed)


def classify_news(news_list: list[str], domains: list[str]) -> dict[str, list[str]]:
    """Classifies a list of news items into specified categories/domains batch-wise.

    Args:
        news_list (list[str]): List of news headlines or articles.
        domains (list[str]): List of allowed category names.

    Returns:
        dict[str, list[str]]: Dictionary with category names as keys and news lists as values.
    """
    aggregated: dict[str, list[str]] = {d: [] for d in domains}
    aggregated["others"] = []

    if not news_list:
        return aggregated

    # Process items in manageable batches (1 per batch if raw full-page text, or 5 if smaller headlines)
    batch_size = 1 if any(len(item) > 2000 for item in news_list) else 5

    for i in range(0, len(news_list), batch_size):
        batch = news_list[i : i + batch_size]
        print(f"  Classifying batch {i // batch_size + 1}/{(len(news_list) + batch_size - 1) // batch_size} ({len(batch)} items)...")
        try:
            batch_result = _classify_single_batch(batch, domains)
            for key, items in batch_result.items():
                if isinstance(items, list):
                    if key not in aggregated:
                        aggregated[key] = []
                    aggregated[key].extend(items)
        except Exception as e:
            print(f"  Error classifying batch {i // batch_size + 1}: {e}")
            aggregated["others"].extend(batch)

    total_classified = sum(len(items) for items in aggregated.values())
    print(f"  Classified {total_classified} total news items across domains.")
    return aggregated

