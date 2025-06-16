# Email Automation

## Project Overview
`send_summary_email.py` sends a spreadsheet via email to a list of recipients. It can be scheduled to distribute automated daily or weekly reports.

## Variables
The script expects environment variables for SMTP credentials and the recipient list. `SMTP_SERVER`, `FROM_ADDR`, and `ATTACHMENT` are constants pointing to the mail server, the sender address and the file to attach.

## Instructions
Install the `python-dotenv` package to load environment variables from a `.env` file. Populate `SMTP_USER`, `SMTP_PASSWORD` and `RECIPIENTS` in that file, then run `python send_summary_email.py`. The script logs in to the SMTP server and sends the email with `summary.xlsx` attached.

## Explanation
A multipart email is composed with `email.mime`. The attachment is read in binary mode and encoded before sending via SMTP. Because recipients are read from the environment, you can easily adjust them without changing the code.
