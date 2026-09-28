import json
from config import API_KEY, MODEL
from langchain_core.tools import tool
from openai import OpenAI

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY)


@tool
def get_top_news_by_category(
    categorized_news: dict[str, list[str]],
    top_n: int = 5,
) -> dict[str, list[str]]:
    """Filters and ranks news items to return the top N news stories per category.

    Args:
        categorized_news (dict[str, list[str]]): Dictionary mapping category names to lists of news items.
        top_n (int): Maximum number of top news items to retain per category (default: 5).

    Returns:
        dict[str, list[str]]: Dictionary with top ranked news items per category.
    """
    ranked_news: dict[str, list[str]] = {}

    for category, news_items in categorized_news.items():
        if not news_items:
            ranked_news[category] = []
            continue

        # If items are already within top_n, keep them directly without extra API call
        if len(news_items) <= top_n:
            ranked_news[category] = news_items
            continue

        prompt = f"""
        You are a senior news editor.
        From the following list of news items under the category '{category}', select the top {top_n} most impactful, important, and distinct news items.
        Rank them from most important to least important.

        News items:
        {json.dumps(news_items, ensure_ascii=False)}

        Return ONLY a valid JSON object in the following format:
        {{
        "top_news": ["item 1", "item 2", ...]
        }}
        """
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a news editor assistant. Return only valid JSON with the selected top news.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            timeout=120,
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)
        ranked_news[category] = parsed.get("top_news", [])[:top_n]

    return ranked_news