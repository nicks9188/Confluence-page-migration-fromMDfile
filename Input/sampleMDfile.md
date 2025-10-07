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


from typing import List, Dict

def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Sort candidates by 'score' descending; ties broken by 'experience_years'.
    """
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
