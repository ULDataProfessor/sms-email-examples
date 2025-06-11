# June Onboarding Video Pipeline

This example demonstrates a basic automation pipeline that generates personalized onboarding
videos for customers who signed up in June 2025. The workflow pulls customer
records from a CRM, creates avatar videos with HeyGen, uploads the videos to
cloud storage, and emails links to the customers.

## Files

- `pipeline.py` – Orchestrates the full workflow.
- `crm_client.py` – Queries the CRM API with date filters and pagination.
- `video_client.py` – Calls the HeyGen avatar API to create a short video.
- `mailer.py` – Sends transactional email with a video link.
- `report.py` – Collects success/failure metrics.
- `requirements.txt` – Required Python packages.

## CRM Query

`CRMClient.query_customers()` accepts `start_date` and `end_date` parameters.
The function issues HTTP GET requests to `$CRM_API_URL/customers` using the
`$CRM_API_KEY` for authentication. Results are paginated by a `next_page`
field in the JSON response, so the client continues fetching pages until no
`next_page` remains.

## Concurrency and Rate Limits

`pipeline.py` processes many customers concurrently using a
`ThreadPoolExecutor`. Because external services may enforce API rate limits,
the pipeline throttles to five video generation calls per second. If more tasks
are queued, execution waits until enough time has passed.

## Configuration

Set the following environment variables before running the pipeline:

- `CRM_API_URL` and `CRM_API_KEY` – Credentials for the CRM service.
- `HEYGEN_API_KEY` – API key for the HeyGen avatar service.
- `S3_BUCKET` or `GCS_BUCKET` – Cloud storage destination for videos.
- `SENDGRID_API_KEY` or SMTP credentials – For sending email.

The email and video templates can be customized by editing the strings in
`video_client.py` and `mailer.py`.

Run the pipeline:

```bash
python pipeline.py
```

