## Smart Recruitment System — Sample Document

> This sample shows headings, tables, code blocks, links, and attachments in Markdown.

**Table of Contents**
- #1-overview
- #2-stakeholders-table
- #3-metrics-table-with-alignment
- #4-code-samples
  - #41-python
  - #42-bash-curl
  - #43-json
- #5-links
- #6-attachments

---

## 1. Overview
The **Smart Recruitment System** streamlines candidate sourcing, screening, and ranking.  
It supports:
- Job requirement capture
- Candidate application intake
- Automated screening and ranking
- Interview scheduling and feedback capture

---

## 2. Stakeholders (Table)

| Stakeholder         | Role                          | Responsibilities                                                                 |
|---------------------|-------------------------------|----------------------------------------------------------------------------------|
| HR Personnel        | Hiring & Compliance           | Define job requirements; shortlist candidates; ensure policy compliance          |
| Interviewers        | Technical/Behavioral Assess   | Conduct interviews; submit scores & feedback                                     |
| Candidates          | Applicants                    | Submit applications; attend interviews; provide requested documentation          |
| System Administrators | Platform Ops               | Manage users; ensure uptime; backups & restores                                  |
| Project Manager     | Delivery Oversight            | Coordinate development, testing, and rollout                                     |

---

## 3. Metrics (Table with alignment)

| Metric                     | Target      | Notes                         |
|:---------------------------|------------:|:------------------------------|
| Time-to-Hire (days)        |          30 | From requisition to acceptance|
| Screening Accuracy (%)     |          90 | % of top candidates identified|
| Interview No-Show Rate (%) |           5 | Lower is better               |

---

## 4. Code Samples

### 4.1 Python

```
from typing import List, Dict

def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    
    Sort candidates by 'score' descending; ties broken by 'experience_years'.
    
    return sorted(
        candidates,
        key=lambda c: (c.get("score", 0), c.get("experience_years", 0)),
        reverse=True
    )

if __name__ == "__main__":
    sample = [
        {"name": "Asha", "score": 86, "experience_years": 4},
        {"name": "Ravi", "score": 86, "experience_years": 6},
        {"name": "Meera", "score": 92, "experience_years": 3},
    ]
    print(rank_candidates(sample))
```
### 4.2 Bash (cURL)
```
# Fetch the latest 5 pages from a Confluence space (example)
curl -s -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  "https://your-site.atlassian.net/wiki/rest/api/content?type=page&spaceKey=CSE&limit=5"
```
### JSON
```
{
  "jobTitle": "Senior Data Engineer",
  "requiredSkills": ["Python", "SQL", "Spark"],
  "minExperienceYears": 5,
  "location": "Mumbai",
  "remoteEligible": true
}
```
## Links
Inline link to Atlassian docs: https://developer.atlassian.com/cloud/confluence/rest/v1/
Reference‑style link: [Confluence Cloud REST API (v2)][confluence-v2]
Internal section link: #6-attachments
https://developer.atlassian.com/cloud/confluence/rest/v2/

## Attachments
Put your files in an attachments/ folder next to this Markdown file, or update the paths below.

### Image (inline)
../Input/attachment/Chacha_Chaudhary.jpg

### Downloadable Files
../Input/attachment/12e3a6_2968e6bf3ac9425f9751696d06c711b7~mv2_d_1584_2032_s_2.jpg
../Input/attachment/33435223.png

***** End of sample document. *****
