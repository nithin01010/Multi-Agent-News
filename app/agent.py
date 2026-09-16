from classify_news import classify_news
from dummy_news import domains, dummy_news
from email_module import send_email
from format import format_news, markdown_to_html

# Step 1: Classify news into domains
print("Step 1: Classifying news...")
classified = classify_news.invoke({"news_list": dummy_news, "domains": domains})
print("Classified:", classified)

# Step 2: Format classified news into newsletter markdown
print("\nStep 2: Formatting newsletter...")
formatted_md = format_news.invoke({"news_data": classified})
print("Formatted markdown ready.")

# Step 3: Convert markdown to HTML
html_body = markdown_to_html(formatted_md)

# Step 4: Send email
print("\nStep 3: Sending email...")
result = send_email.invoke({
    "subject": "Daily Morning Digest",
    "recipients": ["pbhargavreddy3@gmail.com", "nithinmyneni010@gmail.com"],
    "html_body": html_body,
})
print("Email sent!" if result else "Email failed.")
