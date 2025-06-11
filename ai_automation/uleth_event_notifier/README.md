# U of L Event Notifier

This example shows how to pull events from the University of Lethbridge calendar and deliver summaries to students via Slack.

## Files
- `calendar_client.py` – fetches calendar entries and filters them by keyword.
- `summarizer.py` – uses OpenAI to create short friendly blurbs.
- `flyer.py` – generates an event flyer image using a MidJourney style API.
- `notifier.py` – posts the summary and flyer to a Slack channel.
- `requirements.txt` – Python dependencies.

## Calendar Source & Filtering
Specify the RSS or iCal feed URL with the `FEED_URL` environment variable. `calendar_client.fetch_events` downloads the feed and `filter_events` keeps only entries containing the desired faculty or program keywords (e.g. "Business Analytics", "Computer Science").

## Prompt Templates
- **Summary** – The system prompt is:
  `You are a friendly campus assistant who helps students by summarizing events in a cheerful tone.`
- **Image** – The flyer prompt is automatically built from the event title, date and venue:
  `Event flyer for <title> on <date> at <venue>.`

## Subscription Channels
`notifier.send_notification` sends the summary and flyer to Slack using the bot token in `SLACK_BOT_TOKEN` and the channel in `SLACK_CHANNEL`.

To email instead, adapt `notifier.py` to use `smtplib` and your SMTP credentials.

## Running on a Schedule
Install the requirements and set the necessary environment variables (`OPENAI_API_KEY`, `MIDJOURNEY_API_URL`, etc.). Run the scripts manually or schedule them with cron or a workflow tool like Airflow to post updates automatically.
