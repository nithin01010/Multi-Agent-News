from alert import send_failure_alert
from classify_news import classify_news
from email_module import send_email
from format import format_news, markdown_to_html
from news_urls import get_all_image_urls
from image_extracter import extract_from_urls
from rank_news import get_top_news_by_category

domains = ["State", "National", "Global", "Tech & AI", "Sport"]


def run_pipeline():
    # call image urls from differnt news_objects
    print("Gathering news image urls")
    image_urls = get_all_image_urls()
    print("Got all the image urls")

    # Send to Extracter
    print("Extracting news from urls")
    news_list = extract_from_urls(image_urls)
    print("Extracting done")

    # Classify news into domains
    print("Classifying news...")
    classified = classify_news(news_list, domains)
    print("Classification done")

    # Take top N news from each cat
    print("Picking top 5 news from each category")
    top_n_news = get_top_news_by_category(
        categorized_news=classified,
        top_n=5
    )
    print("Picked top 5 news")

    # Format classified news into newsletter markdown
    print("\nFormatting newsletter...")
    formatted_md = format_news(top_n_news)
    print("Formatted markdown ready.")

    # Convert markdown to HTML
    html_body = markdown_to_html(formatted_md)

    # Send email
    print("\nSending email...")
    result = send_email(
        subject="Daily Morning Digest",
        recipients=["pbhargavreddy3@gmail.com", "nithinmyneni010@gmail.com"],
        html_body=html_body,
    )
    print("Email sent!" if result else "Email failed.")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        send_failure_alert(e, context="Standard Agent Pipeline (agent.py)")
        raise
