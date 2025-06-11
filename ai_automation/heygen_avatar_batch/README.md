# HeyGen Avatar Batch Pipeline

This folder demonstrates a basic pipeline for generating video avatars in bulk using the HeyGen API.

## Files

- `avatar_generator.py` – reads an Excel roster and coordinates the avatar creation process
- `poller.py` – simple helper for polling the status endpoint
- `requirements.txt` – minimal dependencies (`openpyxl`, `requests`, `pandas`)

## Excel Template Format

The roster Excel file should contain a sheet with the following columns:

| user_id | name | avatar_template |
| ------- | ---- | --------------- |
| 001 | Alice | friendly_bot |
| 002 | Bob | futuristic |

Each row represents a user profile. `avatar_template` is the HeyGen template ID to use for that user.

## Polling Settings

`poller.Poller` accepts two optional parameters:

- `interval` – seconds to wait between status checks (default `5`)
- `timeout` – maximum seconds to wait before giving up (default `300`)

You can adjust these values in `process_excel()` if your jobs take longer to complete.

## Previewing Videos

Generated videos are downloaded to the `output/` directory with the filename `<user_id>.mp4`. Open the files in any video player to preview the avatars. The CSV `generation_log.csv` records the completion time, status, and video URL returned by HeyGen for later reference.

### Running

Install dependencies and run the script:

```bash
pip install -r requirements.txt
python avatar_generator.py
```

You will be prompted for the path to your Excel roster.
