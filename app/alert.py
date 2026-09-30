from datetime import datetime
import html
import traceback

from email_module import send_email

ADMIN_EMAIL = "nithinmyneni010@gmail.com"


def build_error_html(error_msg: str, context: str, tb_str: str) -> str:
    """Builds a formatted, clean HTML body for failure alerts."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
        padding: 20px;
        margin: 0;
    }}
    .alert-container {{
        max-width: 600px;
        margin: 0 auto;
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #fecaca;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }}
    .header {{
        background-color: #dc2626;
        color: #ffffff;
        padding: 16px 24px;
        font-size: 18px;
        font-weight: 600;
    }}
    .content {{
        padding: 24px;
    }}
    .meta-row {{
        margin-bottom: 12px;
        font-size: 14px;
    }}
    .meta-label {{
        font-weight: 600;
        color: #475569;
    }}
    .error-box {{
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        margin-top: 16px;
        margin-bottom: 16px;
        font-family: monospace;
        font-size: 13px;
        color: #991b1b;
        word-break: break-word;
    }}
    .traceback-box {{
        background-color: #1e293b;
        color: #f8fafc;
        padding: 14px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 12px;
        overflow-x: auto;
        white-space: pre-wrap;
    }}
    .footer {{
        padding: 14px 24px;
        background-color: #f1f5f9;
        font-size: 12px;
        color: #64748b;
        text-align: center;
    }}
</style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            NewsAI Pipeline Execution Failure
        </div>
        <div class="content">
            <div class="meta-row">
                <span class="meta-label">Time:</span> {now_str}
            </div>
            <div class="meta-row">
                <span class="meta-label">Context / Step:</span> {html.escape(context or "General Pipeline Execution")}
            </div>
            <div class="error-box">
                {html.escape(error_msg)}
            </div>
            {f'<div class="meta-label">Traceback:</div><pre class="traceback-box">{html.escape(tb_str)}</pre>' if tb_str else ''}
        </div>
        <div class="footer">
            Automated Alert System &bull; NewsAI
        </div>
    </div>
</body>
</html>"""


def send_failure_alert(
    error: Exception | str,
    context: str = "",
    recipients: list[str] | str | None = None,
) -> bool:
    """Sends a failure alert email to admin recipients with error details and traceback.

    Args:
        error: The caught exception or an error description string.
        context: Name of the script, step, or function where the error occurred.
        recipients: Target email or list of emails. Defaults to ADMIN_EMAIL.

    Returns:
        bool: True if alert email was dispatched, False otherwise.
    """
    if recipients is None:
        recipients = [ADMIN_EMAIL]
    elif isinstance(recipients, str):
        recipients = [recipients]

    if isinstance(error, Exception):
        error_msg = f"{type(error).__name__}: {str(error)}"
        tb_str = traceback.format_exc()
        if tb_str.strip() == "NoneType: None":
            tb_str = ""
    else:
        error_msg = str(error)
        tb_str = traceback.format_exc()
        if tb_str.strip() == "NoneType: None":
            tb_str = ""

    subject = f"[CRITICAL ALERT] NewsAI Execution Failed ({context or 'Pipeline'})"
    html_body = build_error_html(error_msg=error_msg, context=context, tb_str=tb_str)

    print(f"Sending failure alert to {recipients}...")
    return send_email(
        subject=subject,
        recipients=recipients,
        html_body=html_body,
    )
