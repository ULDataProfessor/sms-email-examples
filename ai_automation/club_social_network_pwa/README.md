# Campus Club Connect PWA

This example scaffolds a full stack progressive web app for discovering campus clubs and chatting with other students.  The backend is written with FastAPI and the frontend uses React with Vite.

## Running the Backend

1. Create a `.env` file based on `.env.example` and fill in your secrets.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API server:
   ```bash
   uvicorn backend.app:app --reload
   ```

The API exposes JSON endpoints and a WebSocket channel for real‑time chat. Background tasks update each club's open status from the schedule.

## Running the Frontend

1. Install Node dependencies:
   ```bash
   npm install
   ```
2. Launch the development server:
   ```bash
   npm run dev
   ```

The frontend is a PWA. A service worker caches assets for offline use and enables push notifications when clubs open, new discounts appear, or friends come online.

## Project Structure

- `backend/app.py` – FastAPI application with auth, club data, chat WebSocket and admin ad management.
- `frontend/` – React source with pages, components and a service worker.
- `requirements.txt` – Python packages.
- `package.json` – Node packages for the PWA.

## Usage Scenarios

- Discover clubs, events and discounts.
- Chat in real time with other members.
- Receive push notifications when a favorite club opens or a new ad is posted.
- Admins can upload banner or video ads via the `/ads` endpoint which rotate in the UI.
