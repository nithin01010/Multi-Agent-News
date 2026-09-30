import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import API_KEY, MODEL
from tools import tools

# Initialize LLM (NVIDIA / OpenAI compatible endpoint)
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0.2,
)

SYSTEM_PROMPT = """You are an autonomous news curation and publishing agent.
Your objective:
1. Fetch image URLs for news using `fetch_image_urls`.
2. Extract news text from those images using `extract_news_text`.
3. Classify news into domains: State, National, Global, Tech & AI, Sport using `classify_news_items`.
4. Select the top news items for each category using `rank_news_by_category`.
5. Format into an attractive markdown newsletter digest using `format_newsletter_markdown`.
6. Email the digest to recipients using `send_newsletter_email`.

You have tools to perform every step. Decide tool call sequences autonomously and pass data between tools."""

# Create the autonomous agent using LangGraph's prebuilt ReAct agent
agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    query = (
        "Gather today's news from all sources, extract articles, classify them into "
        "['State', 'National', 'Global', 'Tech & AI', 'Sport'], pick top 5 per category, "
        "and email the formatted digest to pbhargavreddy3@gmail.com and nithinmyneni010@gmail.com."
    )

    print("[*] Starting Autonomous Agent...")
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("\n[Autonomous Agent Completed]")
    print(result["messages"][-1].content)
