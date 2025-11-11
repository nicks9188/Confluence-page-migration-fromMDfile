import os
import requests
import markdownify
from urllib.parse import urlparse

# === Hardcoded credentials ===
EMAIL = "<User_Email>"
PASSWORD = "<User_Password>"  # Use password instead of API token
BASE_URL = "<Confluence_Base_URL>"

# === Source URL (space or page) ===
SOURCE_URL = "<Confluence_Page/Space_url>"

# === Setup ===
auth = (EMAIL, PASSWORD)
headers = {"Accept": "application/json"}
os.makedirs("output", exist_ok=True)

# === Determine if it's a space or page ===
def extract_space_key_or_page_id(url):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if "pages" in parts:
        return "page", parts[-1]
    elif "spaces" in parts:
        idx = parts.index("spaces")
        if idx + 1 < len(parts):
            return "space", parts[idx + 1]
    return None, None

mode, identifier = extract_space_key_or_page_id(SOURCE_URL)

# === Fetch pages ===
pages = []

if mode == "page":
    page_id = identifier
    url = f"{BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    res = requests.get(url, auth=auth, headers=headers)
    if res.status_code == 200:
        data = res.json()
        pages.append(data)

        # Fetch children separately
        children_url = f"{BASE_URL}/rest/api/content/{page_id}/child/page?limit=100&expand=body.storage"
        children_res = requests.get(children_url, auth=auth, headers=headers)
        if children_res.status_code == 200:
            children_data = children_res.json()
            pages.extend(children_data.get("results", []))
        else:
            print("❌ Failed to fetch child pages:", children_res.text)
    else:
        print("❌ Failed to fetch page:", res.text)

elif mode == "space":
    space_key = identifier
    start = 0
    limit = 50
    while True:
        url = f"{BASE_URL}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=body.storage"
        res = requests.get(url, auth=auth, headers=headers)
        if res.status_code == 200:
            data = res.json()
            results = data.get("results", [])
            pages.extend(results)
            if len(results) < limit:
                break
            start += limit
        else:
            print("❌ Failed to fetch space:", res.text)
            break
else:
    print("❌ Invalid URL format.")
    exit()

# === Convert and save ===
for page in pages:
    title = page.get("title", "Untitled").replace("/", "-")
    html = page.get("body", {}).get("storage", {}).get("value", "")
    md = markdownify.markdownify(html, heading_style="ATX")
    with open(f"output/{title}.md", "w", encoding="utf-8") as f:
        f.write(md)

print(f"✅ {len(pages)} pages exported to 'output' folder.")
