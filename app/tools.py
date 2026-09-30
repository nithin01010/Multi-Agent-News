from langchain_core.tools import tool

from classify_news import classify_news as _classify_news
from email_module import send_email as _send_email
from format import format_news as _format_news, markdown_to_html
from image_extracter import extract_from_urls
from news_urls import get_all_image_urls
from rank_news import get_top_news_by_category as _get_top_news_by_category


@tool
def fetch_image_urls() -> list[str]:
    """Fetch newspaper page image URLs from all configured news sources.

    Returns:
        list[str]: A list of image URLs to download and extract.
    """
    print("[*] Gathering news image URLs...")
    urls = get_all_image_urls()
    print(f"[*] Gathered {len(urls)} image URLs.")
    return urls


@tool
def extract_news_text(urls: list[str]) -> list[str]:
    """Extract and transcribe news articles and headlines from newspaper image URLs.

    Args:
        urls (list[str]): List of image URLs of newspaper pages.

    Returns:
        list[str]: Extracted text articles and headlines.
    """
    targets = urls[:2] if urls else []
    print(f"[*] Extracting news text from {len(targets)} images...")
    news = extract_from_urls(targets)
    print(f"[*] Extraction completed ({len(news)} items extracted).")
    return news


@tool
def classify_news_items(news_list: list[str], domains: list[str]) -> dict[str, list[str]]:
    """Classifies a list of news items into specified categories/domains.

    Args:
        news_list (list[str]): List of news headlines or articles.
        domains (list[str]): List of allowed category names (e.g. ['State', 'National', 'Global', 'Tech & AI', 'Sport']).

    Returns:
        dict[str, list[str]]: Dictionary with category names as keys and lists of news items as values.
    """
    print(f"[*] Classifying {len(news_list)} news items into domains...")
    classified = _classify_news(news_list, domains)
    print("[*] Classification completed.")
    return classified


@tool
def rank_news_by_category(
    categorized_news: dict[str, list[str]],
    top_n: int = 5,
) -> dict[str, list[str]]:
    """Filters and ranks news items to pick the top N most important stories per category.

    Args:
        categorized_news (dict[str, list[str]]): Dictionary mapping category names to lists of news items.
        top_n (int): Maximum number of top news items to retain per category (default: 5).

    Returns:
        dict[str, list[str]]: Dictionary containing the top N stories per category.
    """
    print(f"[*] Ranking top {top_n} news items per category...")
    ranked = _get_top_news_by_category(categorized_news, top_n)
    print("[*] Ranking completed.")
    return ranked


@tool
def format_newsletter_markdown(news_data: dict) -> str:
    """Formats categorized news data into a clean, engaging daily morning markdown newsletter.

    Args:
        news_data (dict): Dictionary mapping categories to lists of top news stories.

    Returns:
        str: Formatted markdown text of the newsletter.
    """
    print("[*] Formatting newsletter markdown...")
    formatted = _format_news(news_data)
    print("[*] Newsletter formatting completed.")
    return formatted


@tool
def send_newsletter_email(subject: str, recipients: list[str], markdown_content: str) -> bool:
    """Converts markdown newsletter content to styled responsive HTML and sends it via email.

    Args:
        subject (str): Email subject line.
        recipients (list[str]): List of recipient email addresses.
        markdown_content (str): The markdown formatted newsletter text.

    Returns:
        bool: True if email was successfully sent, False otherwise.
    """
    print(f"[*] Sending email to {recipients}...")
    html_body = markdown_to_html(markdown_content)
    success = _send_email(
        subject=subject,
        recipients=recipients,
        html_body=html_body,
    )
    print("[*] Email sent successfully." if success else "[*] Failed to send email.")
    return success


# All available tools for the autonomous agent
tools = [
    fetch_image_urls,
    extract_news_text,
    classify_news_items,
    rank_news_by_category,
    format_newsletter_markdown,
    send_newsletter_email,
]
