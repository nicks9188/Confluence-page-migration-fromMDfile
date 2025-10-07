#!/usr/bin/env python3
import os
import re
import hashlib
import requests
import markdown

# =========================
# ===== CONFIGURATION =====
# =========================
CONFLUENCE_BASE_URL = "https://<YOUR_CONFLUENCE_DOMAIN_URL>.atlassian.net/wiki"  # no trailing slash required # <-- replace with your confluence url
SPACE_KEY           = "XYZ" # <-- replace with your confluence space code
USERNAME            = "YOUR_EMAIL_ADDRESS" # <-- replace with your email address
API_TOKEN           = "YOUR_API_TOKEN"  # <-- replace with your token
INPUT_FOLDER        = "Input"                # folder containing your .md file(s)

# Insertion behavior
INSERT_POSITION     = "append"               # "append" | "prepend" | "replace"
SECTION_HEADING_LVL = 2                      # 2 => <h2> per file section
SEPARATOR_BETWEEN   = True                   # add <hr/> between blocks
ANCHOR_PREFIX       = "mdfile"               # anchor macro name prefix
HASH_LEN            = 12                     # short hash length for anchors

# =========================
# ====== RENDER HELPERS ===
# =========================

# Detect a pipe-table block (GitHub-style)
_TABLE_HEADER    = re.compile(r'^\s*\|.*\|\s*$')
_TABLE_SEPARATOR = re.compile(r'^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$')

def _is_table_start(lines, i):
    return (
        i + 1 < len(lines)
        and _TABLE_HEADER.match(lines[i])
        and _TABLE_SEPARATOR.match(lines[i + 1])
    )

def wrap_in_panel(html: str) -> str:
    """Wrap an XHTML fragment (e.g., <table>...</table>) in a Confluence panel macro."""
    return (
        '<ac:structured-macro ac:name="panel">'
        '<ac:parameter ac:name="title"></ac:parameter>'
        f'<ac:rich-text-body>{html}</ac:rich-text-body>'
        '</ac:structured-macro>'
    )

def md_block_to_html(md_text: str) -> str:
    """Convert non-table Markdown to HTML (headings, lists, code, etc.)."""
    return markdown.markdown(
        md_text,
        extensions=['fenced_code', 'sane_lists', 'attr_list'],
        output_format='xhtml1'
    )

def md_table_to_html(md_table_block: str) -> str:
    """Convert only the table block to HTML <table> ... </table> (Confluence renders natively)."""
    return markdown.markdown(
        md_table_block,
        extensions=['tables'],
        output_format='xhtml1'
    )

def split_md_segments(md_text: str):
    """
    Yields ('table'|'text', block).
    Table blocks include header, separator, and following pipe rows until a blank line.
    """
    lines = md_text.replace('\r\n', '\n').split('\n')
    i = 0
    while i < len(lines):
        if _is_table_start(lines, i):
            start = i
            i += 2  # header + separator
            while i < len(lines) and '|' in lines[i] and lines[i].strip() != '':
                i += 1
            block = '\n'.join(lines[start:i]).strip('\n')
            yield ('table', block)
            # keep a single blank after table (if present)
            if i < len(lines) and lines[i].strip() == '':
                yield ('text', '\n')
                i += 1
        else:
            start = i
            while i < len(lines) and not _is_table_start(lines, i):
                i += 1
            block = '\n'.join(lines[start:i])
            if block:
                yield ('text', block)

def render_md_tables_and_html_for_rest(md_text: str) -> str:
    """
    Convert tables to HTML (wrapped in a panel), and all other content to HTML.
    Returns a Storage fragment.
    """
    parts = []
    for kind, block in split_md_segments(md_text):
        if kind == 'table':
            table_html = md_table_to_html(block)          # <table>...</table>
            parts.append(wrap_in_panel(table_html))       # keep tables reliable in storage
        else:
            parts.append(md_block_to_html(block))         # headings/lists/paras as HTML
    return ''.join(parts)

def html_heading(text: str, level: int = 2) -> str:
    level = min(max(level, 1), 6)
    # minimal escape for angle brackets
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<h{level}>{text}</h{level}>"

def build_anchor(name: str) -> str:
    return (
        '<ac:structured-macro ac:name="anchor">'
        f'<ac:parameter ac:name="name">{name}</ac:parameter>'
        '</ac:structured-macro>'
    )

def short_hash(text: str, n: int = 12) -> str:
    normalized = text.replace("\r\n", "\n").strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:n]

# =========================
# ====== MAIN LOGIC =======
# =========================
def main():
    # Ask only for Page ID
    page_id = input("Enter the ID of the Confluence page to update: ").strip()
    if not page_id:
        print("No page ID provided.")
        return

    # Gather .md files (sorted)
    if not os.path.isdir(INPUT_FOLDER):
        print(f"Input folder not found: {INPUT_FOLDER}")
        return
    md_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".md")])
    if not md_files:
        print(f"No Markdown files (*.md) found in '{INPUT_FOLDER}'.")
        return

    base = CONFLUENCE_BASE_URL.rstrip("/")
    auth = (USERNAME, API_TOKEN)
    headers = {"Content-Type": "application/json; charset=utf-8"}

    # Fetch existing page
    get_url = f"{base}/rest/api/content/{page_id}?expand=body.storage,version,title"
    r = requests.get(get_url, auth=auth, headers=headers)
    if r.status_code != 200:
        print("Failed to fetch the page:", r.status_code, r.text)
        return

    page = r.json()
    existing = page["body"]["storage"]["value"]
    version  = page["version"]["number"]
    title    = page["title"]

    # Build blocks for each file (skip duplicates by anchor)
    new_blocks = []
    for fname in md_files:
        path = os.path.join(INPUT_FOLDER, fname)
        with open(path, "r", encoding="utf-8") as f:
            md_raw = f.read()

        if not md_raw.strip():
            continue

        # Content-specific anchor (idempotent by content)
        hid   = f"{ANCHOR_PREFIX}-{short_hash(md_raw, HASH_LEN)}"
        anchor = build_anchor(hid)

        # Skip if anchor already present on page (duplicate)
        anchor_regex = re.compile(
            r'<ac:structured-macro[^>]*ac:name="anchor"[^>]*>\s*'
            r'<ac:parameter[^>]*ac:name="name">\s*' + re.escape(hid) + r'\s*</ac:parameter>\s*'
            r'</ac:structured-macro>',
            flags=re.IGNORECASE | re.DOTALL
        )
        if anchor_regex.search(existing):
            print(f"• Skipping '{fname}' (already present).")
            continue

        # Render the file: heading + HTML content
        section_title = os.path.splitext(fname)[0]
        section_head  = html_heading(section_title, SECTION_HEADING_LVL)
        html_fragment = render_md_tables_and_html_for_rest(md_raw)

        block = anchor + section_head + html_fragment
        if SEPARATOR_BETWEEN:
            block = "<hr/>" + block
        new_blocks.append(block)
        print(f"• Prepared '{fname}' for insertion.")

    if not new_blocks:
        print("No new content to add (all files already present or empty).")
        print(f"🔗 {base}/pages/viewpage.action?pageId={page_id}")
        return

    # Decide final page body
    if INSERT_POSITION == "replace":
        updated_body = "".join(new_blocks)
    elif INSERT_POSITION == "prepend":
        updated_body = "".join(new_blocks) + existing
    else:  # default "append"
        updated_body = existing + "".join(new_blocks)

    # Update page
    update_url = f"{base}/rest/api/content/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "space": {"key": SPACE_KEY},
        "body": {"storage": {"value": updated_body, "representation": "storage"}},
        "version": {"number": version + 1}
    }
    u = requests.put(update_url, json=payload, auth=auth, headers=headers)
    if u.status_code == 200:
        print("✅ Page updated successfully.")
        print(f"🔗 {base}/pages/viewpage.action?pageId={page_id}")
    else:
        print("❌ Failed to update page:", u.status_code, u.text)


if __name__ == "__main__":
    main()
