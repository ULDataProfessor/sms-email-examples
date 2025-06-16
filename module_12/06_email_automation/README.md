# Email Automation

**Objective:**  
Send a daily summary email:
- Read `summary.xlsx`
- Attach it to an email
- Send via `smtplib` from `me@example.com` to a list of recipients

**Codex Prompt:**  
“Generate a Python script that uses `smtplib` and `email.mime` to send `summary.xlsx` as an attachment. Use SMTP server `smtp.example.com`, authenticate with environment variables, and send to multiple recipients.”
