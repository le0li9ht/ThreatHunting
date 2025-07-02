# Author: Ashok Krishna Vemuri
import requests
import csv
import re
from bs4 import BeautifulSoup

# === Replace with your HTML source ===
url = 'https://www.cisco.com/c/en/us/td/docs/security/ise/syslog/Cisco_ISE_Syslogs/m_SyslogsList.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# === Prepare regex to extract message fields ===
pattern = re.compile(
    r"Message Code:\s*(\d+)\s+"
    r"Severity:\s*([A-Z]+)\s+"
    r"Message Text:\s*(.+?)\s+"
    r"Message Description:\s*(.+?)\s+"
    r"Local Target Message Format:\s*(.+?)\s+"
    r"Remote Target Message Format:\s*(.+?)(?=\s+Message Code:|\Z)",
    re.DOTALL
)

# === Traverse elements in order ===
entries = []
current_category = None
block_text = ""

for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
    text = tag.get_text(separator="\n", strip=True)

    # Detect category headings (e.g., "Threat Centric NAC")
    if tag.name in ['h1', 'h2', 'h3'] and re.match(r'^[A-Z][A-Za-z\s\-&]+$', text):
        current_category = text.strip()

    # Accumulate blocks under current category
    if "Message Code:" in text:
        block_text = tag.find_parent().get_text(separator="\n", strip=True)
        matches = pattern.findall(block_text)
        for match in matches:
            row = [current_category] + [field.strip() for field in match]
            entries.append(row)

# === Write to CSV ===
with open("cisco_ise_syslog_reference.csv", mode="w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Category", "Message Code", "Severity", "Message Text",
        "Message Description", "Local Target Format", "Remote Target Format"
    ])
    writer.writerows(entries)

print(f"✅ Extracted {len(entries)} entries to cisco_ise_syslog_reference.csv")
