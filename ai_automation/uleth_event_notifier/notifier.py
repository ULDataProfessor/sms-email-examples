import os
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#general")

client = WebClient(token=SLACK_TOKEN)


def send_notification(message: str, image: Optional[bytes] = None, filename: str = "flyer.png") -> None:
    """Post a message and optional image to Slack."""
    try:
        if image:
            client.files_upload(
                channels=SLACK_CHANNEL,
                file=image,
                filename=filename,
                initial_comment=message,
            )
        else:
            client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"Failed to send Slack message: {e}")
