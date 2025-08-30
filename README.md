# PostHog HogQL Counter

Tiny Python CLI to run a HogQL **count** query against PostHog via REST.
Counts events by `target_id` parsed from URL.

## Quick Start

```bash
git clone <repo>
cd <repo>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install requests
```

## Config

```bash
POSTHOG_API_KEY=phx_********               # your API key
POSTHOG_BASE_URL=https://app.posthog.com   # your server url
PROJECT_ID=000                             # project ID
TARGET_ID=4ab8                             # target to find   
```

## Run

```bash
python main.py
# -> Total target_id= 127
```
