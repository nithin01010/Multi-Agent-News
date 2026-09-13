from openai import OpenAI
from email_module import Email
from config import API_KEY
import json
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = API_KEY
)

SYSTEM_PROMPT = """
You are an expert morning news editor and newsletter curator.
Your task is to take categorized raw news items and format them into an engaging, clean, and scannable daily briefing for an email newsletter.

Guidelines:
1. Executive Briefing: Start with a 2-3 bullet point "Today at a Glance" summarizing the biggest stories across all categories.
2. Structure: Group the news under clear category headings (e.g., 🏛️ State, 🇮🇳 National, 🌍 Global, 🤖 Tech & AI).
3. Clarity & Brevity: Polish each headline/item into a crisp, concise 1-2 sentence takeaway with key facts/numbers in **bold**.
4. Tone: Objective, professional, yet engaging.
5. Sign-off: End with an energetic closing line.
"""



def format_news(news_data: dict) -> str:

    user_prompt = f"""
Please format the following categorized news data into a ready-to-read daily morning newsletter:
{json.dumps(news_data, indent=2)}
"""
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=False,
    )
    return completion.choices[0].message.content


def markdown_to_html(markdown_text: str) -> str:
    """Converts markdown text to styled responsive HTML for email."""
    try:
        import markdown
        converted_html = markdown.markdown(markdown_text)
    except ImportError:
        # Fallback if markdown library is not installed
        import html
        converted_html = f"<pre style='white-space: pre-wrap; font-family: inherit;'>{html.escape(markdown_text)}</pre>"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        background-color: #f8fafc;
        margin: 0;
        padding: 20px;
    }}
    .newsletter-container {{
        max-width: 620px;
        margin: 0 auto;
        background: #ffffff;
        padding: 28px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    h1, h2, h3 {{
        color: #0f172a;
        margin-top: 20px;
        margin-bottom: 10px;
    }}
    hr {{
        border: 0;
        height: 1px;
        background-color: #e2e8f0;
        margin: 24px 0;
    }}
    ul {{
        padding-left: 20px;
        margin: 10px 0;
    }}
    li {{
        margin-bottom: 8px;
    }}
    strong {{
        color: #0f172a;
    }}
    .footer {{
        margin-top: 30px;
        text-align: center;
        font-size: 12px;
        color: #94a3b8;
    }}
</style>
</head>
<body>
    <div class="newsletter-container">
        {converted_html}
        <div class="footer">
            Delivered automatically by NewsAI Agent
        </div>
    </div>
</body>
</html>"""


if __name__ == "__main__":
    # Dummy data for testing
    sample_news = {
        "state": [
            "Heavy rainfall expected in coastal districts over the next 48 hours.",
            "State government approves expansion of Metro line Phase 2.",
        ],
        "national": [
            "ISRO prepares for its upcoming solar research payload launch.",
            "Sensex gains 450 points led by banking and tech rally.",
        ],
        "global": [
            "Global summit begins to discuss maritime navigation agreements.",
        ],
        "AI": [
            "NVIDIA announces new open weights model series for enterprise AI.",
        ],
    }
    formatted_output = format_news(sample_news)
    html_output = markdown_to_html(formatted_output)

    # print(formatted_output)
    e = Email()
    e.send_email("Testing", formatted_output, ["nithinmyneni010@gmail.com"], html_output)

