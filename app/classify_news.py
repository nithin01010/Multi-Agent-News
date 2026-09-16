import json

from config import API_KEY, MODEL
from langchain_core.tools import tool
from openai import OpenAI

client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY)


@tool
def classify_news(news_list: list[str], domains: list[str]) -> dict[str, list[str]]:
    """Classifies a list of news items into specified categories/domains.

    Args:
        news_list (list[str]): List of news headlines or articles.
        domains (list[str]): List of allowed category names.

    Returns:
        dict[str, list[str]]: Dictionary with category names as keys and news lists as values.
    """
    prompt = f"""
    Categorize the following news items only into these allowed
    domains: {domains}
    News items:
    {news_list}
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

    result = json.loads(response.choices[0].message.content)
    return result.get("categories", result)
