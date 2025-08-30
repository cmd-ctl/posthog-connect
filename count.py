import requests

# ---- connection ----
POSTHOG_API_KEY = "phx_<...>"
PROJECT_ID = "000"
BASE_URL = "https://posthog.com"

TARGET_ID = "4ab8"

def run_hogql(query: str):
    url = f"{BASE_URL}/api/projects/{PROJECT_ID}/query/"
    headers = {"Authorization": f"Bearer {POSTHOG_API_KEY}", "Content-Type": "application/json"}
    payload = {"query": {"kind": "HogQLQuery", "query": query}}
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

def rows_from(resp_json):
    if "results" in resp_json and isinstance(resp_json["results"], dict):
        return resp_json["results"].get("results", [])
    return resp_json.get("results") or resp_json.get("data") or []

def print_table(rows, header):
    print("\n" + header)
    if not rows:
        print("(пусто)")
        return
    for r in rows:
        print(" | ".join("" if v is None else str(v) for v in r))

CTE = """
WITH
    toString(coalesce(
        properties['$current_url'],
        properties['$screen'],
        properties['$screen_name'],
        ''
    )) AS url_or_screen,
    extractURLParameter(url_or_screen, 'target_id') AS target_id,
    coalesce(properties['prop1'], properties['$prop_1'])   AS p_1,
    coalesce(properties['prop2'], properties['$prop_2']) AS p_2,
    coalesce(properties['prop3'], properties['$prop_3']) AS p_3
"""

def main():
    
    # count
    q_total = f"""
    {CTE}
    SELECT count()
    FROM events
    WHERE target_id = '{TARGET_ID}'
    """
    total = rows_from(run_hogql(q_total))[0][0] if rows_from(run_hogql(q_total)) else 0
    print(f"Total = {TARGET_ID}: {total}")

    

if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        print("HTTP error:", e.response.status_code, e.response.text if e.response is not None else "")
    except Exception as e:
        print("Unexpected error:", e)
